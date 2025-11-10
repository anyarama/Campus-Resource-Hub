const SLOT_INCREMENT_MINUTES = 30;
const DAY_START_MINUTES = 7 * 60; // 7:00 AM
const DAY_END_MINUTES = 22 * 60; // 10:00 PM

class BookingDrawer {
  constructor() {
    this.drawer = document.getElementById('bookingDrawer');
    if (!this.drawer) return;

    this.form = this.drawer.querySelector('[data-booking-form]');
    this.dateInput = this.drawer.querySelector('[data-booking-date]');
    this.purposeInput = this.drawer.querySelector('[data-booking-purpose]');
    this.durationSelect = this.drawer.querySelector('[data-duration-select]');
    this.resetBtn = this.drawer.querySelector('[data-booking-reset]');
    this.slotGrid = this.drawer.querySelector('[data-time-slot-grid]');
    this.messageEl = this.drawer.querySelector('[data-booking-message]');
    this.confirmation = this.drawer.querySelector('[data-booking-confirmation]');
    this.editBtn = this.drawer.querySelector('[data-booking-edit]');
    this.completeBtn = this.drawer.querySelector('[data-booking-complete]');
    this.titleEl = this.drawer.querySelector('[data-booking-title]');

    this.hiddenResourceId = this.drawer.querySelector('[data-booking-resource-id]');
    this.hiddenBookingUrl = this.drawer.querySelector('[data-booking-url]');
    this.hiddenAvailabilityUrl = this.drawer.querySelector('[data-availability-url]');

    this.summaryFields = {
      date: this.drawer.querySelector('[data-summary-date]'),
      time: this.drawer.querySelector('[data-summary-time]'),
      duration: this.drawer.querySelector('[data-summary-duration]'),
      purpose: this.drawer.querySelector('[data-summary-purpose]'),
      note: this.drawer.querySelector('[data-summary-note]'),
    };

    this.currentResource = null;
    this.bookings = [];
    this.requiresApproval = false;
    this.selectedRange = null;
    this.slotButtons = [];

    this.initSlotGrid();
    this.attachGlobalListeners();
    this.attachFormListeners();
    this.setDateBounds();
  }

  attachGlobalListeners() {
    document.addEventListener('click', (event) => {
      const trigger = event.target.closest('[data-booking-open]');
      if (trigger) {
        event.preventDefault();
        this.openDrawer({
          id: trigger.dataset.resourceId,
          title: trigger.dataset.resourceTitle,
          bookingUrl: trigger.dataset.bookingUrl,
          availabilityUrl: trigger.dataset.availabilityUrl,
        });
      }
    });
  }

  attachFormListeners() {
    if (!this.form) return;

    this.form.addEventListener('submit', (event) => {
      event.preventDefault();
      this.handleSubmit();
    });

    this.dateInput?.addEventListener('change', () => {
      this.clearSelection();
      this.fetchAvailability();
    });

    this.durationSelect?.addEventListener('change', () => {
      if (!this.selectedRange) return;
      const requiredSlots = this.getRequiredSlots();
      if (!this.canSelectRange(this.selectedRange.startIndex, requiredSlots)) {
        this.clearSelection();
        this.showMessage('error', 'Not enough time available for that duration.');
      } else {
        this.selectedRange.slots = requiredSlots;
        this.updateSelectionStyles();
        this.updateMessage();
      }
    });

    this.resetBtn?.addEventListener('click', () => {
      this.resetFormState();
      this.fetchAvailability();
    });

    this.editBtn?.addEventListener('click', () => {
      this.showFormView();
    });

    this.completeBtn?.addEventListener('click', () => {
      this.completeBooking();
    });

    document.addEventListener('click', (event) => {
      const closer = event.target.closest('[data-drawer-close]');
      if (closer && this.drawer.contains(closer)) {
        this.resetFormState();
      }
    });
  }

  setDateBounds() {
    if (!this.dateInput) return;
    const today = this.formatDateInput(new Date());
    this.dateInput.min = today;
  }

  initSlotGrid() {
    if (!this.slotGrid) return;
    this.slotGrid.innerHTML = '';
    this.slotButtons = [];
    let index = 0;
    for (let minutes = DAY_START_MINUTES; minutes < DAY_END_MINUTES; minutes += SLOT_INCREMENT_MINUTES) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'time-slot';
      button.dataset.index = String(index);
      button.dataset.minutes = String(minutes);
      button.setAttribute('role', 'gridcell');
      button.setAttribute('aria-pressed', 'false');
      button.textContent = this.formatMinutes(minutes);
      button.addEventListener('click', () => this.handleSlotClick(index));
      this.slotGrid.appendChild(button);
      this.slotButtons.push(button);
      index += 1;
    }
  }

  openDrawer(resource) {
    if (!this.drawer) return;
    this.resetFormState();
    this.currentResource = resource;
    if (this.titleEl) {
      this.titleEl.textContent = `Book ${resource.title}`;
    }
    if (this.hiddenResourceId) this.hiddenResourceId.value = resource.id;
    if (this.hiddenBookingUrl) this.hiddenBookingUrl.value = resource.bookingUrl;
    if (this.hiddenAvailabilityUrl) this.hiddenAvailabilityUrl.value = resource.availabilityUrl;

    const defaultDate = this.formatDateInput(new Date());
    if (this.dateInput) {
      this.dateInput.value = defaultDate;
    }
    this.showMessage('info', 'Select a time to begin.');
    this.fetchAvailability();

    if (window.drawer && typeof window.drawer.open === 'function') {
      window.drawer.open('bookingDrawer');
    } else {
      this.drawer.classList.add('open');
    }
  }

  async fetchAvailability() {
    if (!this.currentResource || !this.dateInput || !this.hiddenAvailabilityUrl) return;
    const dateValue = this.dateInput.value;
    if (!dateValue) {
      this.showMessage('info', 'Pick a date to view availability.');
      return;
    }

    this.setSlotGridBusy(true);
    try {
      const url = new URL(this.hiddenAvailabilityUrl.value, window.location.origin);
      url.searchParams.set('date', dateValue);
      const response = await fetch(url);
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.error || 'Unable to load availability.');
      }
      this.bookings = payload.bookings.map((booking) => ({
        start: new Date(booking.start),
        end: new Date(booking.end),
      }));
      this.requiresApproval = Boolean(payload.requires_approval);
      this.renderAvailability(dateValue);
      this.updateMessage();
    } catch (error) {
      this.bookings = [];
      this.showMessage('error', error.message || 'Failed to load availability.');
      this.disableAllSlots(true);
    } finally {
      this.setSlotGridBusy(false);
    }
  }

  renderAvailability(dateValue) {
    const dateObj = new Date(`${dateValue}T00:00:00`);
    this.slotButtons.forEach((button) => {
      const minutes = Number(button.dataset.minutes);
      const slotStart = this.combineDate(dateObj, minutes);
      const slotEnd = this.combineDate(dateObj, minutes + SLOT_INCREMENT_MINUTES);
      const hasConflict = this.bookings.some((booking) => slotStart < booking.end && slotEnd > booking.start);
      button.disabled = hasConflict;
      button.setAttribute('aria-disabled', hasConflict ? 'true' : 'false');
      button.classList.toggle('is-blocked', hasConflict);
    });
    this.clearSelection();
  }

  disableAllSlots(disabled) {
    this.slotButtons.forEach((button) => {
      button.disabled = disabled;
      button.setAttribute('aria-disabled', disabled ? 'true' : 'false');
      button.classList.toggle('is-blocked', disabled);
      button.classList.remove('is-selected');
    });
    this.selectedRange = null;
  }

  handleSlotClick(index) {
    if (!this.dateInput || !this.dateInput.value) {
      this.showMessage('error', 'Choose a date first.');
      this.dateInput?.focus();
      return;
    }

    const requiredSlots = this.getRequiredSlots();
    if (!this.canSelectRange(index, requiredSlots)) {
      this.showMessage('error', 'Already booked during part of this time.');
      return;
    }

    this.selectedRange = { startIndex: index, slots: requiredSlots };
    this.updateSelectionStyles();
    this.updateMessage();
  }

  canSelectRange(startIndex, slotsNeeded) {
    const endIndex = startIndex + slotsNeeded;
    if (endIndex > this.slotButtons.length) {
      return false;
    }
    for (let i = startIndex; i < endIndex; i += 1) {
      const button = this.slotButtons[i];
      if (!button || button.disabled) {
        return false;
      }
    }
    return true;
  }

  updateSelectionStyles() {
    this.slotButtons.forEach((button, index) => {
      const selected = this.selectedRange
        ? index >= this.selectedRange.startIndex && index < this.selectedRange.startIndex + this.selectedRange.slots
        : false;
      button.classList.toggle('is-selected', Boolean(selected));
      button.setAttribute('aria-pressed', selected ? 'true' : 'false');
    });
  }

  clearSelection() {
    this.selectedRange = null;
    this.slotButtons.forEach((button) => {
      button.classList.remove('is-selected');
      button.setAttribute('aria-pressed', 'false');
    });
  }

  handleSubmit() {
    if (!this.selectedRange) {
      this.showMessage('error', 'Select a time slot first.');
      return;
    }
    if (!this.purposeInput.value.trim()) {
      this.showMessage('error', 'Purpose is required.');
      this.purposeInput.focus();
      return;
    }

    const selection = this.getSelectionWindow();
    if (!selection) {
      this.showMessage('error', 'Invalid time selection.');
      return;
    }

    this.populateSummary(selection);
    this.showConfirmationView();
    this.showMessage('success', 'Slot reserved! Complete booking to finalize.');
    if (window.toast?.success) {
      window.toast.success('Time slot drafted! Complete the booking to finish.');
    }
  }

  populateSummary(selection) {
    const { dateLabel, timeLabel, durationLabel, purposeLabel, noteLabel } = selection;
    if (this.summaryFields.date) this.summaryFields.date.textContent = dateLabel;
    if (this.summaryFields.time) this.summaryFields.time.textContent = timeLabel;
    if (this.summaryFields.duration) this.summaryFields.duration.textContent = durationLabel;
    if (this.summaryFields.purpose) this.summaryFields.purpose.textContent = purposeLabel;
    if (this.summaryFields.note) this.summaryFields.note.textContent = noteLabel;
  }

  showFormView() {
    if (!this.form || !this.confirmation) return;
    this.form.hidden = false;
    this.confirmation.hidden = true;
  }

  showConfirmationView() {
    if (!this.form || !this.confirmation) return;
    this.form.hidden = true;
    this.confirmation.hidden = false;
  }

  completeBooking() {
    if (!this.currentResource) return;
    const selection = this.getSelectionWindow();
    if (!selection) return;
    const params = new URLSearchParams();
    params.set('resource_id', this.currentResource.id);
    params.set('date', selection.dateISO);
    params.set('start', selection.startTime);
    params.set('end', selection.endTime);
    params.set('duration', selection.durationMinutes);
    if (this.purposeInput?.value) {
      params.set('purpose', this.purposeInput.value.trim());
    }
    window.location.href = `${this.currentResource.bookingUrl}?${params.toString()}`;
  }

  updateMessage() {
    if (!this.selectedRange) {
      this.clearMessage();
      if (this.requiresApproval) {
        this.showMessage('info', 'Requires approval: owner will confirm before booking.');
      }
      return;
    }

    if (this.requiresApproval) {
      this.showMessage('info', 'Requires approval: owner will review this request.');
    } else {
      this.clearMessage();
    }
  }

  showMessage(type, text) {
    if (!this.messageEl) return;
    this.messageEl.textContent = text;
    this.messageEl.dataset.state = type;
    this.messageEl.hidden = false;
  }

  clearMessage() {
    if (!this.messageEl) return;
    this.messageEl.textContent = '';
    this.messageEl.removeAttribute('data-state');
    this.messageEl.hidden = true;
  }

  resetFormState() {
    this.bookings = [];
    this.requiresApproval = false;
    this.clearSelection();
    this.clearMessage();
    if (this.form) {
      this.form.hidden = false;
      this.form.reset();
    }
    if (this.confirmation) {
      this.confirmation.hidden = true;
    }
    this.durationSelect.value = '60';
  }

  setSlotGridBusy(isBusy) {
    if (!this.slotGrid) return;
    this.slotGrid.classList.toggle('is-loading', isBusy);
  }

  getRequiredSlots() {
    const duration = parseInt(this.durationSelect.value, 10) || SLOT_INCREMENT_MINUTES;
    return Math.max(1, Math.ceil(duration / SLOT_INCREMENT_MINUTES));
  }

  getSelectionWindow() {
    if (!this.selectedRange || !this.dateInput || !this.dateInput.value) return null;
    const startMinutes = Number(this.slotButtons[this.selectedRange.startIndex].dataset.minutes);
    const durationMinutes = this.selectedRange.slots * SLOT_INCREMENT_MINUTES;
    const endMinutes = startMinutes + durationMinutes;
    const dateObj = new Date(`${this.dateInput.value}T00:00:00`);
    const startDate = this.combineDate(dateObj, startMinutes);
    const endDate = this.combineDate(dateObj, endMinutes);
    return {
      dateISO: this.dateInput.value,
      dateLabel: startDate.toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' }),
      timeLabel: `${this.formatTime(startDate)} – ${this.formatTime(endDate)}`,
      durationLabel: `${durationMinutes} minutes`,
      purposeLabel: this.purposeInput.value.trim(),
      noteLabel: this.requiresApproval ? 'Requires approval' : 'Auto-approve',
      startTime: this.formatTime24(startDate),
      endTime: this.formatTime24(endDate),
      durationMinutes,
    };
  }

  combineDate(base, minutes) {
    const combined = new Date(base);
    combined.setHours(0, minutes, 0, 0);
    return combined;
  }

  formatMinutes(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    const date = new Date();
    date.setHours(hours, mins, 0, 0);
    return this.formatTime(date);
  }

  formatTime(date) {
    return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
  }

  formatTime24(date) {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
  }

  formatDateInput(date) {
    return date.toISOString().split('T')[0];
  }
}

window.addEventListener('DOMContentLoaded', () => {
  new BookingDrawer();
});
