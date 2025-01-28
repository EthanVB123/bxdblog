function createBlogPost(title, imageUrl, postUrl) {
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

    // Add to results container
    const resultsContainer = document.getElementById('results');
    resultsContainer.appendChild(blogPost);

    return blogPost;
}
createBlogPost('First Blog Post', 'comingsoon.jpg', 'https://google.com');
createBlogPost('Second Blog Post', 'comingsoon.jpg', 'https://google.com'); 
createBlogPost('Third Blog Post', 'comingsoon.jpg', 'https://google.com');

