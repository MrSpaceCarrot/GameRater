<script setup>
  // Libraries & Components
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/AuthStore';
  import apiClient from '@/axios';

  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faSteam } from '@fortawesome/free-brands-svg-icons';
  import { faBoxOpen, faGamepad } from '@fortawesome/free-solid-svg-icons';
  library.add(faSteam, faBoxOpen, faGamepad);

  import VueSlider from 'vue-slider-component'
  import 'vue-slider-component/theme/default.css'
  import Tagify from '@yaireo/tagify'
  import '@yaireo/tagify/dist/tagify.css'
  import NavBar from '../components/NavBar.vue'

  // Variables
  // Auth
  const authStore = useAuthStore();
  const token = ref(authStore.token);

  // Form fields
  let gamename = ref("");
  let gamelink = ref("");
  let gamebannerlink = ref("");
  let platform = ref("Roblox");
  let linkformat = ref("https://www.roblox.com/games/xxxxxxxxx");
  let submissionloading = ref(false);

  // Form messages
  let submissionmessage = ref(null);
  let submissionmessagetype = ref(null);

  // Form Slider
  let sliderValues = ref([1, 16]);
  let marks = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]);

  // Tagify
  const tagify = ref(null);
  const tags = ref([]);
  
  // Functions
  // Capitalize first letter
  function capitalizeFirstLetter(value) {
    return String(value).charAt(0).toUpperCase() + String(value).slice(1);
  }

  // Change tab contents when clicked
  function updatePlatform(selectedPlatform) {
    // Clear form is current tab is clicked
    if(selectedPlatform != platform.value) {clearForm()}
    platform.value = selectedPlatform;

    // Clear submission message
    submissionmessage.value = '';
    submissionmessagetype.value = '';

    // Change link format depending on platform
    if (selectedPlatform == "Roblox") {
      linkformat.value = "https://www.roblox.com/games/xxxxxxxxx";
    } else if (selectedPlatform == "Steam") {
      linkformat.value = "https://store.steampowered.com/app/xxxxxxx";
    } else if (selectedPlatform == "Party") {
      linkformat.value = "https://jackbox.tv (or other)";
    } else {
      linkformat.value = "https://game link here";
    }
  }

  // Clear all fields of form
  function clearForm() {
    gamename.value = "";
    gamelink.value = "";
    gamebannerlink.value = "";
    sliderValues.value = [1, 16];
    tagify.value.removeAllTags();
  }

  // Submit game form
  function submitGame() {
    // Collect tags into list
    let tags = []
    for(let tag of document.getElementsByClassName("tagify__tag")) {
      tags.push(tag.getAttribute("title"))
    }

    // Collect data object
    const data = {
      "name": gamename.value,
      "platform": platform.value,
      "link": gamelink.value,
      "banner_link": gamebannerlink.value,
      "min_party_size": sliderValues.value[0],
      "max_party_size": sliderValues.value[1],
      "tags": tags
    };

    // Form checking
    if(data["name"] == "") { submissionmessage.value = "Name is required"; submissionmessagetype.value = "Error"; return;}
    if(data["platform"] == "") { submissionmessage.value = "Platform is required"; submissionmessagetype.value = "Error"; return;}
    if(data["link"] == "") { submissionmessage.value = "Link is required"; submissionmessagetype.value = "Error"; return;}
    if(data["banner_link"] == null && data["platform"] == "Party" || data["banner_link"] == '' && data["platform"] == "Other") { submissionmessage.value = `Banner link is required for ${platform.value} games`;submissionmessagetype.value = "Error"; return;}
    if(data["min_party_size"] < 1 || data["max_party_size"] > 16) { submissionmessage.value = "Invalid party size"; submissionmessagetype.value = "Error"; return;}
    if(data["tags"].length < 2 || data["tags"] > 5) { submissionmessage.value = "Please choose between 2 and 5 tags"; submissionmessagetype.value = "Error"; return;}
    submissionloading.value = true;

    //Send request
    apiClient.post("/games/add", data, {headers: {Authorization: `Token ${token.value}`}})
    .then((response) => {
      submissionmessage.value = `Successfully added game: ${response.data["name"]}`;
      submissionmessagetype.value = "Success";
      submissionloading.value = false;
    })
    .catch((error) => {
      const data = error["response"]["data"]
      for (const key in data) {
        if (data.hasOwnProperty(key)) {
          const value = data[key][0];
          submissionmessage.value = `${capitalizeFirstLetter(key)}: ${capitalizeFirstLetter(value)}`
        }
      }
      submissionmessagetype.value = "Error";
      submissionloading.value = false; 
    });
  } 

  // Mounted
  onMounted(() => {
    // Create tagify
    let input = document.getElementById('gametags');
    tagify.value = new Tagify(input, {maxTags: 5, whitelist: [], enforceWhitelist: true, dropdown: {enabled: 1, maxItems: 50, enabled: 0, closeOnSelect: false}});

    // Get and set whitelist for tagify
    apiClient.get("/games/tags", {headers: {Authorization: `Token ${token.value}`}})
    .then((response) => {
      for(let tag of response.data) {tags.value.push(tag["tag"])}
      tagify.value.whitelist = tags.value
    })
    .catch((error) => {console.log(error)});
  });
</script>

<template>
  <NavBar />
  <div class="container px-5">
    <h2 class="text-light py-2">Add Game</h2>

    <form @submit.prevent="submitGame">
        <!-- Platform selection-->
        <ul class="nav nav-tabs nav-justified mb-1" role="tablist">
            <li class="nav-item">
                <a @click="updatePlatform('Roblox')" class="nav-link active" id="roblox-tab" href="" data-bs-toggle="tab" role="tab">Roblox
                  <img src="/roblox.svg" alt="Roblox Logo" class="inline-svg">
                </a>
            </li>
            <li class="nav-item">
                <a @click="updatePlatform('Steam')" class="nav-link" id="steam-tab" href="" data-bs-toggle="tab" role="tab">Steam
                  <font-awesome-icon icon="fa-brands fa-steam" />
                </a>
            </li>
            <li class="nav-item">
                <a @click="updatePlatform('Party')" class="nav-link" id="party-tab" href="" data-bs-toggle="tab" role="tab">Party
                  <font-awesome-icon icon="fa-solid fa-box-open" />
                </a>
            </li>
            <li class="nav-item">
                <a @click="updatePlatform('Other')" class="nav-link" id="other-tab" href="" data-bs-toggle="tab" role="tab">Other
                  <font-awesome-icon icon="fa-solid fa-gamepad" />
                </a>
            </li>
        </ul>
        <!-- /Platform selection-->

        <!-- Submission message-->
        <div v-if="submissionmessage && submissionmessagetype==='Error'" class="py-2 my-3 bg-danger text-center rounded">
          <h6>{{ submissionmessage }}</h6>
        </div>
        <div v-if="submissionmessage && submissionmessagetype==='Success'" class="py-2 my-3 bg-success text-center rounded">
          <h6>{{ submissionmessage }}</h6>
        </div>
        <!-- /Submission message -->

        <!-- Entry fields-->
        <!-- Game Name -->
        <div class="mb-2 mt-2">
            <label class="form-label text-light"><h5>Name:</h5></label>
            <input v-model="gamename" type="text" class="form-control formquery" value="" placeholder="Game name">
        </div>
        <!-- /Game Name -->

        <!-- Game Link-->
        <div class="mb-3">
            <label class="form-label text-light"><h5>Link</h5></label>
            <input v-model="gamelink" type="text" class="form-control formquery" value="" :placeholder=linkformat>
        </div>
        <!-- /Game Link-->

        <!-- Game Banner Link-->
        <div v-if="platform==='Party' || platform==='Other'" class="mb-3">
            <label class="form-label text-light"><h5>Banner Link</h5></label>
            <p class="formcomments">Please provide a suitable banner image for the game, prefered size 768x432. If the game is in jackbox, you may get images from <a href="https://www.jackboxgames.com/games" target="_blank">here</a></p>
            <input v-model="gamebannerlink" type="text" class="form-control formquery"  value="" placeholder="Banner link">
        </div>
        <!-- /Game Banner Link-->

        <!-- Game Party Size-->
        <div class="mb-5">
            <label for="gamepartysize" class="form-label text-light"><h5>Required Party Size</h5></label>
            <vue-slider 
              v-model="sliderValues"
              :min="1"
              :max="16"
              :interval="1"
              :adsorb="true"
              :marks="marks"
              :contained="true"
              :tooltip="'none'"
            ></vue-slider>
        </div>
        <!-- /Game Party Size-->

        <!-- Game Tags-->
        <div class="mb-4">
            <label for="gametags" class="form-label text-light"><h5>Tags</h5></label>
            <p class="formcomments">Please add 2-5 tags that best describe the game</p>
            <input class="form-control tagifyinput" id='gametags' name="gametags">
        </div>
        <!-- /Game Tags-->
        <!-- /Entry fields-->
        
        <button type="submit" class="btn btn-primary" :class="{ disabled: submissionloading }">
          Add Game
          <span v-if="submissionloading===true" class="spinner-border spinner-border-sm"></span>
        </button>
    </form> 
  </div>
</template>

<style>

/* Platform tabs and form*/
#roblox-tab.active {
  background: #e42818;
}

#steam-tab.active {
  background: #2a475e;
}

#party-tab.active {
  background: #4854f4;
}

#other-tab.active {
  background: rgb(5, 88, 5);
}

#roblox-tab, #steam-tab, #party-tab, #other-tab {
  color: #fff;
  border: 1px;
}

#roblox-tab.active, #steam-tab.active, #party-tab.active, #other-tab.active {
  color: #fff;
}

input.formquery, input.formquery[type=text] {
  background-color: #505560 !important;
  color: white;
  border: none;
  box-shadow: none !important;
  outline: none !important;
}

.formcomments {
  color: #bebebe !important;
}

.vue-slider-mark-label {
  color: #fff;
}

h6 {
  margin-bottom: 0px;
}

.submittedgameimage {
  max-height: 200px;
}

/* Tagify */

.tagify__input, .tagify {
  background-color: #505560 !important;
  color: white !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}

.tagifyinput, .tagifyinput .tagify__tag {
  --tag-bg: #E5E5E5;
  --tag-hover: #E5E5E5;
  --tag-remove-bg: #E5E5E5;
  --tag-inset-shadow-size: 1.3em;
}

.tagify__input, .tagify__tag {
  margin-top: 2.4px;
  margin-bottom: 2.4px;
}

.tagify__dropdown__item {
  display: inline-block;
}

.tagify__dropdown__item--active {
  background-color: #f8f9fa !important;
  color: #000;
}

.tagify__tag:hover {
  text-decoration: none !important;
}

.tagify__dropdown__wrapper, .tagify__dropdown, .tagify__dropdown__footer{
  color: white;
  background-color: #6c757d !important;
}

.tagify__input, .tagify {
  border-top-right-radius: 0.375rem !important;
  border-bottom-right-radius: 0.375rem !important;
}

.tagify__tag-text {
  color: #000 !important;
}

</style>