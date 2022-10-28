document.addEventListener('DOMContentLoaded', function () {
   var colors = ["rgba(234, 4, 126, 0.5)", "rgba(255, 109, 40, 0.5)", "rgba(252, 231, 0, 0.5)", "rgba(0, 245, 255, 0.5)"];
   var cardHead = document.querySelectorAll(".card-header");
   var cardDivider = document.querySelectorAll(".todo-div");
   var card = document.querySelectorAll('.todo-card');
   for (i = 0; i < cardHead.length; i++) {
      var c = colors[Math.floor(Math.random() * colors.length)];
      cardHead[i].style.backgroundColor = c;
      cardDivider[i].style.backgroundColor = c;
      card[i].style.boxShadow = "0 0 0.5em 0.5em " + c;
   }
});


document.addEventListener('DOMContentLoaded', function () {
   var actionButton = document.getElementById('menu-button');
   var menu = document.getElementById('action-menu')

   //addEventListener - attaches an event handler to the specified element.
   actionButton.addEventListener('click', () => {
      menu.classList.toggle('show-menu');
   });
});

document.addEventListener('DOMContentLoaded', () => {
   // Functions to open and close a modal
   function openModal($el, id, name) {
      $el.classList.add('is-active');
      modalId = $el.querySelector('#task_id');
      modalName = $el.querySelector('#name');
      modalId.value = id;
      modalName.value = name;
   }

   function closeModal($el) {
      $el.classList.remove('is-active');
   }

   function closeAllModals() {
      (document.querySelectorAll('.modal') || []).forEach(($modal) => {
         closeModal($modal);
      });
   }

   // Add a click event on buttons to open a specific modal
   (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
      const modal = $trigger.dataset.target;
      const id = $trigger.dataset.id
      const name = $trigger.dataset.name
      const $target = document.getElementById(modal);

      $trigger.addEventListener('click', () => {
         openModal($target, id, name);
      });
   });
   // Add a click event on various child elements to close the parent modal
   (document.querySelectorAll('.delete, .button') || []).forEach(($close) => {
      const $target = $close.closest('.modal');

      $close.addEventListener('click', () => {
         closeModal($target);
      });
   });

   // Add a keyboard event to close all modals
   document.addEventListener('keydown', (event) => {
      const e = event || window.event;

      if (e.keyCode === 27) { // Escape key
         closeAllModals();
      }
   });
});

document.addEventListener('DOMContentLoaded', function () {
   var raisedDate = document.getElementById('raised');
   n = new Date();
   y = n.getFullYear();
   m = n.getMonth() + 1;
   d = n.getDate();
   raisedDate.value = d + "/" + m + "/" + y;
});