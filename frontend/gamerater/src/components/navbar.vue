<template>
<nav class="navbar navbar-expand-lg p-0">
    <div class="container-fluid bg-dark navbar-dark d-flex align-items-center">
        <div class="d-flex align-items-center flex-grow-1">

            <a class="navbar-brand" href="">
                <img src="/favicon.ico" alt="Site Logo" class="sitelogo">
            </a>

            <a class="text-light navbar-brand" href="all"><h2>Derps Inc Gaming</h2></a>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav d-flex align-items-center">
                    <li class="nav-item px-3">
                        <a class="nav-link nooverflow" href="">All Games</a>
                    </li>
                    <li class="nav-item px-3">
                        <a class="nav-link nooverflow" href="">Add Game</a>
                    </li>
                    <li class="nav-item px-3">
                        <a class="nav-link nooverflow" href="">Top Rated</a>
                    </li>
                    <li class="nav-item px-3">
                        <a class="nav-link nooverflow" href="">Your Ratings</a>
                    </li>
                </ul>

                <form class="d-flex input-group-sm mainsearchbar me-3">
                    <input class="form-control me-2 mainsearchbarquery" type="text" placeholder="Search">
                </form>
            </div>
        </div>

        <ul class="navbar-nav d-flex align-items-center">
            <li class="nav-item">
                <div class="d-flex align-items-center">
                    <a class="nav-link text-light" href="">
                        <img src="https://cdn.discordapp.com/avatars/725251028999602239/432cbf5d267767e56bb79bdb0a727bf2?size=1024" class="usericon rounded-circle" alt="User Avatar">
                    </a>
                    <a class="nav-link text-light logoutbutton ms-2" href="">
                        <img src="/logout.svg" class="inline-svg">
                    </a>
                </div>
            </li>
        </ul>

    </div>
</nav>
</template>

<style>
.sitelogo {
    max-height: 50px;
    width: auto;
}

.usericon {
    max-height: 30px;
    width: auto;
}

.mainsearchbar {
    flex-grow: 0;
    flex-basis: 40%;
}

input.mainsearchbarquery, input.mainsearchbarquery[type=text]{
    background-color: #505560;
    color: white;
    border: none;
    box-shadow: none !important;
    outline: none !important;
}

.nooverflow {
    white-space: nowrap
}

.inline-svg {
    width: 1.1em;
    height: 1.1em;
    vertical-align: middle;
    margin-top: -3px;
}
</style>