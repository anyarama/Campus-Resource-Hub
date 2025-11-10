class BulkTableController {
  constructor(form) {
    this.form = form;
    this.master = form.querySelector('[data-bulk-master]');
    this.checkboxes = Array.from(form.querySelectorAll('[data-bulk-checkbox]'));
    this.countLabel = form.querySelector('[data-bulk-count]');
    this.actionInput = form.querySelector('[data-bulk-action-input]');
    this.actionButtons = Array.from(form.querySelectorAll('[data-bulk-action]'));
    this.rows = this.checkboxes.map((box) => box.closest('tr'));
    this.bindEvents();
    this.updateState();
  }

  bindEvents() {
    if (this.master) {
      this.master.addEventListener('change', () => {
        const checked = this.master.checked;
        this.checkboxes.forEach((checkbox) => {
          checkbox.checked = checked;
          this.toggleRow(checkbox.closest('tr'), checked);
        });
        this.updateState();
      });
    }

    this.checkboxes.forEach((checkbox) => {
      checkbox.addEventListener('change', () => {
        this.toggleRow(checkbox.closest('tr'), checkbox.checked);
        this.updateState();
      });
    });

    this.rows.forEach((row, index) => {
      const checkbox = this.checkboxes[index];
      if (!row || !checkbox) return;
      row.addEventListener('keydown', (event) => {
        if (event.code === 'Space') {
          event.preventDefault();
          checkbox.checked = !checkbox.checked;
          this.toggleRow(row, checkbox.checked);
          this.updateState();
        }
      });
      row.addEventListener('click', (event) => {
        const target = event.target;
        if (target instanceof HTMLInputElement) return;
        if (target && target.closest('button, a, label')) return;
        checkbox.checked = !checkbox.checked;
        this.toggleRow(row, checkbox.checked);
        this.updateState();
      });
    });

    this.actionButtons.forEach((button) => {
      button.addEventListener('click', (event) => {
        const selected = this.getSelectedCount();
        if (selected === 0) {
          event.preventDefault();
          return;
        }
        if (this.actionInput) {
          this.actionInput.value = button.value;
        }
      });
    });
  }

  toggleRow(row, isSelected) {
    if (!row) return;
    row.classList.toggle('is-selected', Boolean(isSelected));
  }

  getSelectedCount() {
    return this.checkboxes.filter((checkbox) => checkbox.checked).length;
  }

  updateState() {
    const selectedCount = this.getSelectedCount();
    const total = this.checkboxes.length;
    if (this.countLabel) {
      this.countLabel.textContent = `${selectedCount} selected`;
    }
    if (this.master) {
      this.master.indeterminate = selectedCount > 0 && selectedCount < total;
      this.master.checked = selectedCount === total && total > 0;
    }
    this.actionButtons.forEach((button) => {
      button.disabled = selectedCount === 0;
    });
  }
}

function initBulkForms() {
  const forms = document.querySelectorAll('[data-bulk-form]');
  forms.forEach((form) => new BulkTableController(form));
}

window.addEventListener('DOMContentLoaded', initBulkForms);
