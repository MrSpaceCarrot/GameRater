<script>
  import axios from 'axios';

  import VueSlider from 'vue-slider-component'
  import 'vue-slider-component/theme/default.css'
  import Tagify from '@yaireo/tagify'
  import '@yaireo/tagify/dist/tagify.css'

  import NavBar from '../components/NavBar.vue'

  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faSteam } from '@fortawesome/free-brands-svg-icons';
  import { faPencil } from '@fortawesome/free-solid-svg-icons';
  import { faGamepad } from '@fortawesome/free-solid-svg-icons';

  library.add(faSteam, faPencil, faGamepad);

  export default {
    name: 'Add',
    components: {
      NavBar,
      VueSlider,
      FontAwesomeIcon
    },
    data() {
      return {
        // Auth
        token: localStorage.getItem('token'),
        apiUrl: import.meta.env.VITE_API_URL,

        // Form
        gamename: '',
        gamelink: '',
        gamebannerlink: '',
        platform: "Roblox",
        linkformat: "https://www.roblox.com/games/xxxxxxxxx",
        submissionloading: false,

        // Form messages
        submissionmessage: '',
        submissionmessagetype: '',
        submissionresponse: '',

        // Slider
        sliderValues: [2, 16],
        marks: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],

        // Tagify
        tagify: '',
        tags: []
      }
    },
    mounted() {
      // Check if user is logged in
      if(!this.token) {
        this.$router.push({name: 'Login', params: { message: 'missingtoken'} });
      }
      axios.get(this.apiUrl + "/auth/verifytoken", {headers: {Authorization: `Token ${this.token}`}})
      .catch((error) => {this.$router.push({name: 'Login', params: { message: 'invalidtoken'} });});

      // Setup tagify
      this.setupTagify()
    },
    methods: {
      capitalizeFirstLetter(value) {
        return String(value).charAt(0).toUpperCase() + String(value).slice(1);
      },

      // Setup tagify
      setupTagify() {
        // Create tagify
        var input = document.getElementById('gametags');
        this.tagify = new Tagify(input, {
          maxTags: 5,
          whitelist: [],
          enforceWhitelist: true,
          dropdown: {
            enabled: 1, 
            maxItems: 50,
            enabled: 0, 
            closeOnSelect: false
            }
          },
        );

        // Get whitelist
        axios.get(this.apiUrl + "/tags", {headers: {Authorization: `Token ${this.token}`}})
        .then((response) => {
          for(let tag of response.data) {
            this.tags.push(tag["tag"])
          }
          this.tagify.whitelist = this.tags
        })
        .catch((error) => {console.log(error)});
      },

      // Change tab contents when clicked
      updatePlatform(selectedPlatform) {
        if(selectedPlatform != this.platform) {
          this.clearForm()
        }
        this.platform = selectedPlatform

        switch (this.platform) {
          case "Roblox":
            this.linkformat = "https://www.roblox.com/games/xxxxxxxxx"
            break
          case "Steam":
            this.linkformat = "https://store.steampowered.com/app/xxxxxxx"
            break
          case "Party":
            this.linkformat = "https://jackbox.tv (or other)"
            break
          case "Other":
            this.linkformat = "https://game link here"
            break
        }

        this.submissionmessage = '',
        this.submissionmessagetype = ''
      },

      // Clear all fields
      clearForm() {
        this.gamename = ''
        this.gamelink = ''
        this.gamebannerlink = ''
        this.sliderValues = [2, 16]
        this.tagify.removeAllTags()
      },

      // Submit game form
      submitGame() {
        // Collect tags into list
        var tags = []
        for(let tag of document.getElementsByClassName("tagify__tag")) {
          tags.push(tag.getAttribute("title"))
        }

        // Collect data object
        const data = {
          "name": this.gamename,
          "platform": this.platform,
          "link": this.gamelink,
          "banner_link": this.gamebannerlink,
          "min_party_size": this.sliderValues[0],
          "max_party_size": this.sliderValues[1],
          "tags": tags
        };

        // Form checking
        if(data["name"] == ''){ this.submissionmessage = "Name is required"; this.submissionmessagetype = "Error"; return}
        if(data["platform"] == ''){ this.submissionmessage = "Platform is required"; this.submissionmessagetype = "Error"; return}
        if(data["link"] == ''){ this.submissionmessage = "Link is required"; this.submissionmessagetype = "Error"; return}
        if(data["banner_link"] == '' && data["platform"] == "Party" || data["banner_link"] == '' && data["platform"] == "Other"){ this.submissionmessage = "Banner link is required for " + this.platform + " games"; this.submissionmessagetype = "Error"; return}
        if(data["min_party_size"] < 2 || data["max_party_size"] > 16){ this.submissionmessage = "Invalid party size"; this.submissionmessagetype = "Error"; return}
        if(data["tags"].length < 2 || data["tags"] > 5){ this.submissionmessage = "Please choose between 2 and 5 tags"; this.submissionmessagetype = "Error"; return}

        this.submissionloading = true;

        //Send request
        axios.post(this.apiUrl + "/games/add", data, {headers: {Authorization: `Token ${this.token}`}})
        .then((response) => {
          this.submissionresponse = response;
          this.submissionmessage = "Successfully added game: " + response.data["name"];
          this.submissionmessagetype = "Success";
          this.submissionloading = false;
        })
        .catch((error) => {
          const data = error["response"]["data"]
          for (const key in data) {
            if (data.hasOwnProperty(key)) {
              const value = data[key][0];
              this.submissionmessage = `${this.capitalizeFirstLetter(key)}: ${this.capitalizeFirstLetter(value)}`
            }
          }

          this.submissionmessagetype = "Error";
          this.submissionloading = false; 
        });
        
      } 
    },
  }
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
                  <font-awesome-icon icon="fa-solid fa-pencil" />
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
              :min="2"
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
        
        <button type="submit" class="btn btn-primary">
          Add Game
          <span v-if="submissionloading===true" class="spinner-border spinner-border-sm"></span>
        </button>
    </form> 
  </div>
</template>

<style>

/* Message */

/* Platform tabs and form*/
#roblox-tab.active {
  background: #e42818;
}

#steam-tab.active {
  background: #2a475e ;
}

#party-tab.active {
  background: #4854f4
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

.inline-svg {
  width: 1.1em;
  height: 1.1em;
  vertical-align: middle;
  margin-top: -3px;
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

.tagify {
  width: 100%;
  padding: 0rem 0.1rem;
  font-size: 1rem; 
  line-height: 1.5;
  height: calc(2.25rem); 
  display: flex;
  align-items: center;
}

.tagify__input, .tagify {
  background-color: #505560 !important;
  color: white !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}

.tagify__input {
  display: inline-block;
  align-self: center;
  vertical-align: middle;
  margin: 0px !important;
}

.tagify__tag {
  display: inline-flex;
  margin: 2px !important;
  padding: 0px !important;
}

.tagify__tag:hover {
  text-decoration: none !important;
}

.tagify__dropdown__item {
  background-color: #505560 !important;
  color: white;
}

.tagify__dropdown__item--active {
  background-color: #2f6ac3 !important;
}

.tagify__dropdown__wrapper, .tagify__dropdown, .tagify__dropdown__footer{
  color: white;
  background-color: #484b52 !important;
}

.tagifyinput, .tagifyinput .tagify__tag {
  --tag-bg: #E5E5E5;
  --tag-hover: #E5E5E5;
  --tag-remove-bg: #E5E5E5;
  --tag-inset-shadow-size: 1.3em;
}

</style>