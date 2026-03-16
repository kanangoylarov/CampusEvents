// Simple client-side filtering for Events page
document.addEventListener('DOMContentLoaded', function () {
  const eventsList = document.getElementById('eventsList');
  if (!eventsList) return;

  const cards = Array.from(eventsList.querySelectorAll('.event-card'));
  const filterButtons = Array.from(document.querySelectorAll('.filter-btn, .filter-tab')).filter(
    function (btn) {
      return !!btn.dataset.filter;
    }
  );
  const searchInput = document.getElementById('eventSearch');
  const advancedPanel = document.getElementById('advancedFilter');

  const today = new Date();
  const todayStr = [
    today.getFullYear(),
    String(today.getMonth() + 1).padStart(2, '0'),
    String(today.getDate()).padStart(2, '0')
  ].join('-');

  let activeFilter = 'all';
  let searchTerm = '';

  function normalize(value) {
    return String(value || '').trim().toLowerCase();
  }

  function matchesFilter(card) {
    const startDate = normalize(card.dataset.startDate);
    const category = normalize(card.dataset.category);

    if (activeFilter === 'all') {
      return true;
    }

    if (activeFilter === 'today') {
      return !!startDate && startDate === todayStr;
    }

    if (activeFilter.indexOf('category:') === 0) {
      const wantedCategory = normalize(activeFilter.slice('category:'.length));
      return !!category && category === wantedCategory;
    }

    return true;
  }

  function matchesSearch(card) {
    if (!searchTerm) {
      return true;
    }

    const title = normalize(card.dataset.title) || normalize(card.dataset.name);
    return title.indexOf(searchTerm) !== -1;
  }

  function applyFilters() {
    cards.forEach(function (card) {
      const visible = matchesFilter(card) && matchesSearch(card);
      card.style.display = visible ? '' : 'none';
    });
  }

  filterButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (btn.classList.contains('filter-tab-more')) {
        if (advancedPanel) {
          advancedPanel.style.display =
            advancedPanel.style.display === 'none' || advancedPanel.style.display === '' ? 'block' : 'none';
        }
        return;
      }

      activeFilter = btn.dataset.filter || 'all';
      filterButtons.forEach(function (item) {
        item.classList.remove('active');
      });
      btn.classList.add('active');
      applyFilters();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', function () {
      searchTerm = normalize(searchInput.value);
      applyFilters();
    });
  }

  applyFilters();
});
