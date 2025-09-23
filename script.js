document.addEventListener("DOMContentLoaded", function () {
  const currentUrl = encodeURIComponent(window.location.href);
  const pageTitle = encodeURIComponent(document.title);

  const shareLinks = {
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${currentUrl}`,
    tiktok: `https://www.tiktok.com/share?url=${currentUrl}`,
    whatsapp: `https://api.whatsapp.com/send?text=${pageTitle}%20${currentUrl}`,
    telegram: `https://t.me/share/url?url=${currentUrl}&text=${pageTitle}`,
    twitter: `https://twitter.com/intent/tweet?text=${pageTitle}&url=${currentUrl}`,
    reddit: `https://www.reddit.com/submit?url=${currentUrl}&title=${pageTitle}`
  };

  document.querySelectorAll(".share-buttons a").forEach(button => {
    button.addEventListener("click", function (e) {
      e.preventDefault();

      const platform = this.className;
      const appUrl = this.getAttribute("href");
      const fallbackUrl = shareLinks[platform];

      window.location.href = appUrl;

      setTimeout(() => {
        window.open(fallbackUrl, "_blank");
      }, 800);
    });
  });
});
