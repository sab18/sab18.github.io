// menu.js
document.addEventListener("DOMContentLoaded", function() {
  if (typeof menuList === 'undefined') {
    console.error('menuList is not defined.');
    return;
  }
  // Find the menu container in the header
  var menuContainer = document.querySelector('.menu-container');
  if (!menuContainer) {
    console.error('No .menu-container found in the document.');
    return;
  }
  let menu = '<ul style="display:flex;gap:24px;list-style:none;margin:0;padding:0;">';
  for (const item of menuList) {
    menu += `<li><a href="${item.file}" style="color:#F5F1E8;font-size:18px;text-decoration:none;padding:8px 12px;transition:background 0.2s;border-radius:2px;">${item.label}</a></li>`;
  }
  menu += '</ul>';
  menuContainer.innerHTML = menu;
});
