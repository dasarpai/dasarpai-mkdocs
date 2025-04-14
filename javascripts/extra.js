// docs/javascripts/extra.js
document.addEventListener("DOMContentLoaded", function () {
    const categories = document.querySelectorAll(".category");
  
    categories.forEach((category) => {
      const summary = category.querySelector("summary");
      if (!summary) return;
      
      const categoryName = summary.textContent.trim();
      const savedState = localStorage.getItem("category_" + encodeURIComponent(categoryName));
  
      // Set initial state based on localStorage
      if (savedState === "open") {
        category.open = true;
      } else {
        category.open = false;
      }
  
      // Toggle and save state on click
      summary.addEventListener("click", function () {
        setTimeout(() => {
          const isOpen = category.open;
          localStorage.setItem(
            "category_" + encodeURIComponent(categoryName),
            isOpen ? "open" : "closed"
          );
        }, 0);
      });
    });
  });