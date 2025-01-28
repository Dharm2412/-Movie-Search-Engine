import streamlit as st
import requests
import pandas as pd

# Configure the app
st.set_page_config(page_title="Movie Search", layout="wide")

# API configuration
API_URL = "https://ott-details.p.rapidapi.com/advancedsearch"
HEADERS = {
    "x-rapidapi-host": "ott-details.p.rapidapi.com",
    "x-rapidapi-key": "9074604315msh06db58e0bb2ff26p182b6cjsna6fa352250af"
}

# Sidebar for filters
with st.sidebar:
    st.header("🎬 Movie Filters")

    # Create filters
    year_range = st.slider(
        "Select Year Range",
        1970, 2020, (2000, 2020)
    )

    imdb_range = st.slider(
        "IMDb Rating Range",
        0.0, 10.0, (6.0, 7.8),
        step=0.1
    )

    genre = st.selectbox(
        "Genre",
        ["action", "comedy", "drama", "horror", "romance", "thriller"]
    )

    language = st.selectbox(
        "Language",
        ["english", "hindi", "spanish", "french", "german"]
    )

    content_type = st.selectbox(
        "Content Type",
        ["movie", "series"]
    )

# Main content area
st.title("🎥 Movie Search Engine")
st.markdown("Discover movies and TV shows based on your preferences!")

# Prepare parameters
params = {
    "start_year": year_range[0],
    "end_year": year_range[1],
    "min_imdb": imdb_range[0],
    "max_imdb": imdb_range[1],
    "genre": genre,
    "language": language,
    "type": content_type,
    "sort": "latest",
    "page": 1
}

# Add pagination controls
col1, col2, _ = st.columns([1, 1, 5])
with col1:
    if st.button("⏮ Previous Page"):
        params["page"] = max(1, params["page"] - 1)
with col2:
    if st.button("Next Page ⏭"):
        params["page"] += 1

# Show loading spinner
with st.spinner("Searching for movies..."):
    try:
        # Make API request
        response = requests.get(API_URL, headers=HEADERS, params=params)
        data = response.json()

        if response.status_code == 200 and data.get("results"):
            # Display results
            for movie in data["results"]:
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        # Display movie poster or placeholder
                        poster = movie.get("imageurl", ["https://via.placeholder.com/150x200?text=No+Image"])[0]
                        st.image(poster, width=200)

                    with col2:
                        st.subheader(movie.get("title", "Untitled"))
                        st.markdown(f"**IMDb Rating:** ⭐ {movie.get('imdbrating', 'N/A')}")
                        st.markdown(f"**Released:** {movie.get('released', 'N/A')}")
                        st.markdown(f"**Runtime:** {movie.get('runtime', 'N/A')}")
                        st.markdown(f"**Synopsis:** {movie.get('synopsis', 'No description available')}")

                    st.markdown("---")

            st.success(f"Found {len(data['results'])} results on page {params['page']}")

        else:
            st.warning("No results found. Try adjusting your filters.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")