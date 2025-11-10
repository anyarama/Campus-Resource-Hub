class MessagesApp {
  constructor() {
    this.thread = document.querySelector('[data-thread]');
    this.form = document.querySelector('[data-composer]');
    this.textarea = this.form ? this.form.querySelector('[data-composer-input]') : null;
    this.conversationLinks = document.querySelectorAll('[data-conversation-link]');

    this.init();
  }

  init() {
    if (this.thread) {
      this.scrollThreadToBottom();
    }

    this.bindComposer();
    this.bindConversationLinks();
  }

  scrollThreadToBottom() {
    requestAnimationFrame(() => {
      this.thread.scrollTop = this.thread.scrollHeight;
    });
  }

  bindComposer() {
    if (!this.form) return;

    this.form.addEventListener('keydown', (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
        event.preventDefault();
        this.form.requestSubmit();
      }
    });

    if (this.textarea) {
      const autoResize = () => {
        this.textarea.style.height = 'auto';
        this.textarea.style.height = `${Math.min(this.textarea.scrollHeight, 220)}px`;
      };
      this.textarea.addEventListener('input', autoResize);
      autoResize();
      this.textarea.focus();
    }

    const attachTrigger = this.form.querySelector('[data-attach-trigger]');
    const attachInput = this.form.querySelector('[data-attach-input]');
    if (attachTrigger && attachInput) {
      attachTrigger.addEventListener('click', () => attachInput.click());
      attachInput.addEventListener('change', () => {
        if (!attachInput.files.length) return;
        const fileName = attachInput.files[0].name;
        const hint = document.querySelector('.composer-hint');
        if (hint) {
          hint.textContent = `${fileName} attached (not sent)`;
        }
      });
    }
  }

  bindConversationLinks() {
    this.conversationLinks.forEach((link) => {
      link.addEventListener('click', () => {
        link.classList.remove('is-unread');
        const badge = link.querySelector('[data-unread-badge]');
        if (badge) {
          badge.remove();
        }
      });
    });
  }
}

window.addEventListener('DOMContentLoaded', () => {
  new MessagesApp();
});
