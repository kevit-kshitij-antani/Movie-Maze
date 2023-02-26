const axios = require("axios");
const { response } = require("express");
const { PythonShell } = require("python-shell");
const { spawn } = require("child_process");

const fetch_poster_url = `https://api.themoviedb.org/3/movie/0?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US`;

async function moveById(movie_id) {
  const details = await fetch_details(movie_id);
  const poster = await fetch_poster(movie_id);
  const reviews = await fetch_reviews(movie_id);
  const cast = await fetch_cast(movie_id);
  const trailer = await fetch_trailer(movie_id);
  return {
    details,
    poster,
    reviews,
    cast,
    trailer
  }
}

async function recommender(movie_id) {
  const pythonScriptPath = "python/recommend.py";
  const modelFilePath = "python/similarity.pkl";

  const movie = movie_id;

  // let pyshell = new PythonShell(pythonScriptPath);
  // pyshell.send(modelFilePath);

  // pyshell.send(inputData)

  // let option = {
  //   mode:'text',
  //   pythonOptions: ["-u"],
  //   scriptPath: "python",
  //   args: [19995],
  // };

  // PythonShell.run("recommend.py", option)
  //   .then((messages) => {
  //     // results is an array consisting of messages collected during execution
  //     console.log("results: %j", messages);
  //   })
  //   .catch((e) => {
  //     console.log(e);
  //   });

  var process = spawn("python", ["-u","python/recommend.py", movie]);
  return process

}

const Response = recommender(19995);
console.log(Response)

Response.stdout.on("data", function (data) {
  console.log(data)
  return data.toString();
});

async function fetch_details(movie_id) {
  const response = await axios.get(
    `https://api.themoviedb.org/3/movie/${movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US`
  );
  return response.data;
}

async function fetch_poster(movie_id) {
  const response = await axios.get(
    `https://api.themoviedb.org/3/movie/${movie_id}/?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US`
  );
  return `https://image.tmdb.org/t/p/w500/${response.data.belongs_to_collection.poster_path}`;
}

async function fetch_reviews(movie_id) {
  const response = await axios.get(
    `https://api.themoviedb.org/3/movie/${movie_id}/reviews?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US`
  );
  const reviews = response.data.results;
  const movieReviews = [];
  for (let review of reviews) {
    movieReviews.push(review.content);
  }
  console.log(movieReviews);
  return movieReviews;
}

async function fetch_cast(movie_id) {
  const response = await axios.get(
    `https://api.themoviedb.org/3/movie/${movie_id}/credits?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US`
  );
  const crews = response.data.cast;
  console.log(crews[0]);
  const cast = [];
  for (let crew of crews) {
    if (crew.known_for_department == "Acting") {
      cast.push(crew.original_name);
    }
  }
  console.log(cast);
  return cast;
}

async function fetch_trailer(movie_id) {
  const response = await axios.get(
    `https://api.themoviedb.org/3/movie/${movie_id}/videos?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US`
  );
  const results = response.data.results;
  let video = "";
  for (let item of results) {
    if (item.type === "Trailer") {
      const key = item.key;
      video = `https://www.youtube.com/watch?v=${key}`;
      console.log("+++++", video);
      return video;
    }
  }

  if (video === "") {
    const key = results[0].key;
    video = `https://www.youtube.com/watch?v=${key}`;
    return video;
  }
}


module.exports = {
  moveById
};
