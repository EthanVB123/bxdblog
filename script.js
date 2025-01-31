async function search() { // Perform a semantic search on the blog posts
    const query = document.getElementById('search-input').value;
    try {
        const response = await fetch(`http://127.0.0.1:5000/callSearch?query=${encodeURIComponent(query)}`);
        const resultJSON = await response.json();
        console.log("Output from Python:", resultJSON);
        renderSearchResults(resultJSON.result); // Render the search results using the existing renderSearchResults function
    } catch (error) {
        console.error("Error:", error);
        // Clear results and show error message
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = '<p class="error">An error occurred while searching. Please try again.</p>';
    }
}

// Create an event listener for the search button
document.getElementById('search-button').addEventListener('click', search);
// Create an event listener for the search input to search on enter
document.getElementById('search-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        search();
    }
});

function createBlogPost(title, imageUrl, postUrl, distance = undefined) {
    // Create main container
    const blogPost = document.createElement('div');
    blogPost.className = 'blog-post';
    blogPost.onclick = () => window.location.href = postUrl;

    // Create and set up image
    const img = document.createElement('img');
    img.src = imageUrl;
    img.alt = 'Blog post thumbnail';

    // Create and set up title
    const titleElement = document.createElement('h2');
    titleElement.className = 'post-title';
    titleElement.textContent = title;

    // Assemble the blog post
    blogPost.appendChild(img);
    blogPost.appendChild(titleElement);

    // Add distance if specified
    if (distance !== undefined) {
        const distanceElement = document.createElement('p');
        distanceElement.className = 'distance';
        distanceElement.style.fontSize = 'small';
        
        // Calculate color based on distance
        let color;
        if (distance <= 1) {
            color = '#006400'; // Dark green
        } else if (distance >= 2) {
            color = '#8B0000'; // Dark red
        } else {
            // Linear interpolation between colors for values between 1 and 2
            const t = (distance - 1) / (2 - 1); // Normalize to 0-1
            const r = Math.round(0 * (1 - t) + 139 * t);
            const g = Math.round(100 * (1 - t) + 0 * t);
            const b = Math.round(0 * (1 - t) + 0 * t);
            color = `rgb(${r}, ${g}, 0)`;
        }
        
        distanceElement.style.color = color;
        distanceElement.textContent = `distance: ${distance}`;
        blogPost.appendChild(distanceElement);
    }

    // Add to results container
    const resultsContainer = document.getElementById('results');
    resultsContainer.appendChild(blogPost);

    return blogPost;
}

function renderSearchResults(searchResults) {
    // Clear existing results
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';

    // Render each search result as a blog post
    console.log("Search Results:", searchResults);
    for (let i = 0; i < searchResults.length; i++) {
        const result = searchResults[i];
        const [title, distance, url] = result; // Destructure the tuple to get title and distance
        createBlogPost(title, 'comingsoon.jpg', url, distance);
    }
}


search();

