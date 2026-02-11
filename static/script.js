const contentData = [
    {
        id: 1,
        title: "Cosmic Odyssey",
        genre: "Sci-Fi",
        year: 2025,
        rating: 8.7,
        img: 'https://upload.wikimedia.org/wikipedia/en/1/17/Cosmic_Odyssey_TPB_Cover.jpg'
    },

    {
        id: 2,
        title: "The Lion King",
        genre: "Adventure",
        year: 2024,
        rating: 8.5,
        img: "https://upload.wikimedia.org/wikipedia/en/3/3d/The_Lion_King_poster.jpg"

    },

    {
        id: 3,
        title: "Avatar",
        genre: "Science fiction",
        year: 2026,
        rating: 9.4,
        img: "https://upload.wikimedia.org/wikipedia/en/5/54/Avatar_The_Way_of_Water_poster.jpg"
    },

    {
        id: 4,
        title: "Star_Wars",
        genre: "Fantasy",
        year: 2022,
        rating: 9,
        img: "https://en.wikipedia.org/wiki/Star_Wars:_The_Rise_of_Skywalker#/media/File:Star_Wars_The_Rise_of_Skywalker_poster.jpg"
    },

    {
        id: 5,
        title: "Harry_Potter_and_the_Philosopher_Stone",
        genre: "Adventure",
        year: 2025,
        rating: 8.3,
        img: "https://en.wikipedia.org/wiki/Harry_Potter_and_the_Philosopher%27s_Stone_%28film%29#/media/File:Harry_Potter_and_the_Philosopher's_Stone_banner.jpg"
    },

    {
        id: 6,
        title: "Squid_Game_Season_1",
        genre: "Action",
        rating: 8,
        img: "https://en.wikipedia.org/wiki/Squid_Game_season_1#/media/File:Squid_Game_season_1_poster.png"
    }
];


function generateCards(containerId, items) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    items.forEach(item => {
        const card = document.createElement("div");
        card.className = "movie-card";
        card.dataset.id = item.id;

        card.innerHTML = `
            <div class="movie-poster">
                <img src="${item.img}" alt="${item.title}">
                <div class="movie-rating">${item.rating}</div>
            </div>

            <div class="movie-info">
                <h3 class="movie-title">${item.title}</h3>
                <div class="movie-meta">
                    <span>${item.genre}</span>
                    <span>${item.year || item.season || ""}</span>
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}


document.addEventListener('DOMContentLoaded', () => {
    const movies = contentData.filter(item => item.year);
    const tvShows = contentData.filter(item => item.season);

    generateCards('movieGrid', movies);
    generateCards('tvGrid', tvShows);
});




 