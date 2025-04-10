document.addEventListener('DOMContentLoaded', async function() {
  const dsblogListingPlaceholder = document.querySelector('#dsblog-listing-placeholder');
  if (!dsblogListingPlaceholder) return;

  try {
    // Fetch all markdown files from the dsblog directory
    const response = await fetch('/dsblog/');
    const html = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    
    // Extract links to all markdown files
    const links = Array.from(doc.querySelectorAll('a[href$=".md"], a[href$="/"]'))
      .filter(link => !link.href.includes('..') && !link.textContent.includes('..'));
    
    // Create grid container
    const gridContainer = document.createElement('div');
    gridContainer.className = 'dsblog-grid';
    
    // Process each article
    const articlePromises = links.map(async link => {
      try {
        const articleUrl = link.href;
        const articleResponse = await fetch(articleUrl);
        const articleHtml = await articleResponse.text();
        const articleDoc = parser.parseFromString(articleHtml, 'text/html');
        
        // Extract article metadata
        const title = articleDoc.querySelector('h1')?.textContent || 
                      articleDoc.querySelector('h2')?.textContent || 
                      link.textContent.replace('.md', '').replace(/-/g, ' ');
        
        const content = articleDoc.querySelector('.md-content__inner');
        const paragraphs = content ? Array.from(content.querySelectorAll('p')) : [];
        const excerpt = paragraphs.length > 0 ? paragraphs[0].textContent.substring(0, 150) + '...' : '';
        
        // Estimate reading time (average reading speed: 200 words per minute)
        const articleText = content ? content.textContent : '';
        const wordCount = articleText.split(/\s+/).length;
        const readingTime = Math.max(1, Math.ceil(wordCount / 200));
        
        // Create article card
        const card = document.createElement('div');
        card.className = 'dsblog-card';
        
        // Generate a thumbnail based on title (placeholder)
        const thumbnailUrl = `https://source.unsplash.com/300x200/?${encodeURIComponent(title.split(' ').slice(0, 2).join(' '))}`;
        
        card.innerHTML = `
          <div class="dsblog-thumbnail">
            <img src="${thumbnailUrl}" alt="${title}">
          </div>
          <div class="dsblog-content">
            <h3>${title}</h3>
            <div class="dsblog-meta">
              <span class="dsblog-reading-time">${readingTime} min read</span>
            </div>
            <p class="dsblog-excerpt">${excerpt}</p>
            <a href="${articleUrl}" class="dsblog-read-more">Read More</a>
          </div>
        `;
        
        return card;
      } catch (err) {
        console.error('Error processing article:', err);
        return null;
      }
    });
    
    // Wait for all article processing to complete
    const articleCards = await Promise.all(articlePromises);
    
    // Add valid cards to the grid
    articleCards.filter(card => card !== null).forEach(card => {
      gridContainer.appendChild(card);
    });
    
    // Replace placeholder with grid
    dsblogListingPlaceholder.replaceWith(gridContainer);
    
  } catch (error) {
    console.error('Error loading dsblog articles:', error);
    dsblogListingPlaceholder.innerHTML = '<p>Error loading blog articles. Please try again later.</p>';
  }
});
