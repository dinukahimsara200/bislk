/* ── BisLK main.js ──────────────────────────── */

document.addEventListener('DOMContentLoaded', function () {

  /* ─────────────────────────────────────────────
     1. DYNAMIC EXTENSION FIELDS
     Watches the category dropdown on the Add
     Business form. Reveals the correct extension
     fieldset (restaurants / hotels / salons) and
     hides the others.
  ───────────────────────────────────────────── */
  const catSelect = document.getElementById('category_id');
  if (catSelect) {
    catSelect.addEventListener('change', function () {
      const slug = this.options[this.selectedIndex]
                       .getAttribute('data-slug') || '';
      document.querySelectorAll('.ext-fields').forEach(el => {
        el.classList.remove('active');
      });
      const target = document.getElementById('ext-' + slug);
      if (target) target.classList.add('active');
    });
    // Trigger on page load for edit mode / browser back
    catSelect.dispatchEvent(new Event('change'));
  }


  /* ─────────────────────────────────────────────
     2. INTERACTIVE STAR RATING WIDGET
     Converts the hidden rating input into 5
     clickable stars on the review form.
  ───────────────────────────────────────────── */
  const ratingInput  = document.getElementById('rating');
  const starsWrapper = document.getElementById('star-widget');

  if (ratingInput && starsWrapper) {
    starsWrapper.innerHTML = '';
    for (let i = 1; i <= 5; i++) {
      const star = document.createElement('i');
      star.className   = 'fa fa-star star-btn me-1';
      star.dataset.val = i;
      star.style.cursor   = 'pointer';
      star.style.fontSize = '1.6rem';
      star.style.color    = '#ddd';
      star.style.transition = 'color 0.12s';
      starsWrapper.appendChild(star);
    }

    function paintStars(val) {
      starsWrapper.querySelectorAll('.star-btn').forEach(s => {
        s.style.color = parseInt(s.dataset.val) <= val ? '#f5a623' : '#ddd';
      });
    }

    starsWrapper.querySelectorAll('.star-btn').forEach(star => {
      star.addEventListener('mouseenter', () => paintStars(star.dataset.val));
      star.addEventListener('mouseleave', () => paintStars(ratingInput.value || 0));
      star.addEventListener('click', () => {
        ratingInput.value = star.dataset.val;
        paintStars(star.dataset.val);
      });
    });

    // Restore on load if value pre-set
    paintStars(ratingInput.value || 0);
  }


  /* ─────────────────────────────────────────────
     3. IMAGE FALLBACK
     Replaces broken <img> tags with a grey
     placeholder div so the layout never breaks.
  ───────────────────────────────────────────── */
  document.querySelectorAll('img[data-fallback]').forEach(img => {
    img.addEventListener('error', function () {
      this.src = '/static/img/placeholder.jpg';
    });
  });


  /* ─────────────────────────────────────────────
     4. AUTO-DISMISS FLASH ALERTS  (4 seconds)
  ───────────────────────────────────────────── */
  setTimeout(() => {
    document.querySelectorAll('.alert.fade.show').forEach(el => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert.close();
    });
  }, 4000);


  /* ─────────────────────────────────────────────
     5. RATING BAR ANIMATION  (business detail)
     Animates the width of review breakdown bars
     on page load.
  ───────────────────────────────────────────── */
  document.querySelectorAll('.rating-bar-fill').forEach(bar => {
    const target = bar.getAttribute('data-width') || '0';
    bar.style.width = '0%';
    setTimeout(() => {
      bar.style.transition = 'width 0.6s ease';
      bar.style.width      = target + '%';
    }, 200);
  });

});