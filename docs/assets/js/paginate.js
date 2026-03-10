// paginate.js — client-side paginator for Jekyll collections
// Usage: initPaginator({ listId: 'my-list', pageSize: 20 })
(function () {
  function initPaginator(opts) {
    var listEl = document.getElementById(opts.listId);
    if (!listEl) return;

    var items = listEl.querySelectorAll('[data-index]');
    var pageSize = opts.pageSize || 20;
    var totalItems = items.length;
    var totalPages = Math.ceil(totalItems / pageSize);

    if (totalPages <= 1) return; // nothing to paginate

    var currentPage = 0; // 0-based internally

    function showPage(page) {
      var start = page * pageSize;
      var end = start + pageSize;
      for (var i = 0; i < items.length; i++) {
        items[i].style.display = (i >= start && i < end) ? '' : 'none';
      }
      currentPage = page;
      renderControls();
    }

    function renderControls() {
      var ctrl = document.getElementById(opts.listId + '-pagination');
      if (!ctrl) return;

      var prevDisabled = currentPage === 0;
      var nextDisabled = currentPage === totalPages - 1;

      ctrl.innerHTML =
        '<button class="pagination-btn' + (prevDisabled ? ' pagination-btn--disabled' : '') + '" id="' + opts.listId + '-prev" ' + (prevDisabled ? 'disabled' : '') + '>&larr; Newer</button>' +
        '<span class="pagination-info">Page ' + (currentPage + 1) + ' of ' + totalPages + '</span>' +
        '<button class="pagination-btn' + (nextDisabled ? ' pagination-btn--disabled' : '') + '" id="' + opts.listId + '-next" ' + (nextDisabled ? 'disabled' : '') + '>Older &rarr;</button>';

      var prevBtn = document.getElementById(opts.listId + '-prev');
      var nextBtn = document.getElementById(opts.listId + '-next');

      if (prevBtn && !prevDisabled) {
        prevBtn.addEventListener('click', function () {
          showPage(currentPage - 1);
          listEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
      }
      if (nextBtn && !nextDisabled) {
        nextBtn.addEventListener('click', function () {
          showPage(currentPage + 1);
          listEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
      }
    }

    showPage(0);
  }

  window.initPaginator = initPaginator;
})();
