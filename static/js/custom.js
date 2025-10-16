document.addEventListener('DOMContentLoaded', function() {
      const inputs = document.querySelectorAll('.custom-input input');
      
      inputs.forEach(input => {
        const label = input.nextElementSibling;
        const container = input.parentElement;
        
        // Ensure label starts in default position
        if (!input.value) {
          label.style.top = '50%';
          label.style.fontSize = '16px';
          label.style.transform = 'translateY(-50%)';
        }
        
        // On focus
        input.addEventListener('focus', function() {
          if (!this.value) {
            label.style.top = '0';
            label.style.fontSize = '12px';
          }
          container.classList.add('focused');
        });
        
        // On blur
        input.addEventListener('blur', function() {
          if (!this.value) {
            label.style.top = '50%';
            label.style.fontSize = '16px';
            label.style.transform = 'translateY(-50%)';
          }
          container.classList.remove('focused');
        });
        
        // Update label position when typing
        input.addEventListener('input', function() {
          if (this.value) {
            label.style.top = '0';
            label.style.fontSize = '12px';
          }
        });
        input.addEventListener('change', function() {
          if (this.value) {
            label.style.top = '0';
            label.style.fontSize = '12px';
          }
        });
      });
    });




    document.addEventListener('DOMContentLoaded', () => {
      const uploader = document.querySelector('.file-uploader');
      const input = uploader.querySelector('input[type="file"]');
      const label = uploader.querySelector('label');

      input.addEventListener('focus', () => {
        uploader.classList.add('focused');
        label.style.top = '0';
        label.style.fontSize = '12px';
      });

      input.addEventListener('blur', () => {
        if (!input.value) {
          uploader.classList.remove('focused');
          label.style.top = '50%';
          label.style.fontSize = '16px';
          label.style.transform = 'translateY(-50%)';
        }
      });

      input.addEventListener('change', () => {
        if (input.value) {
          uploader.classList.add('focused');
          label.style.top = '0';
          label.style.fontSize = '12px';
        }
      });
    });



    