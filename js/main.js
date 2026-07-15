/* REDS site interactions — nav, GSAP reveals, contact form */

(function () {
  "use strict";

  const header = document.querySelector(".site-header");
  const nav = document.querySelector(".site-nav");
  const toggle = document.querySelector(".nav-toggle");
  const form = document.querySelector("#contact-form");

  /* Sticky header shadow */
  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Mobile nav */
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* Hero ready class for gentle zoom settle */
  const hero = document.querySelector(".hero");
  if (hero) {
    requestAnimationFrame(() => hero.classList.add("is-ready"));
  }

  /* Contact form — static only */
  if (form) {
    const status = document.querySelector("#form-status");
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const name = form.querySelector('[name="name"]');
      const email = form.querySelector('[name="email"]');
      const subject = form.querySelector('[name="subject"]');
      const message = form.querySelector('[name="message"]');

      if (!name.value.trim() || !email.value.trim() || !message.value.trim()) {
        if (status) {
          status.textContent = "Please fill in your name, email, and message.";
          status.classList.add("is-error");
        }
        return;
      }

      const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
      if (!emailOk) {
        if (status) {
          status.textContent = "Please enter a valid email address.";
          status.classList.add("is-error");
        }
        return;
      }

      if (status) {
        status.classList.remove("is-error");
        status.textContent =
          "Thank you. Your message has been prepared. (Demo form — no server connected.)";
      }

      const body = [
        `Name: ${name.value.trim()}`,
        `Email: ${email.value.trim()}`,
        "",
        message.value.trim(),
      ].join("\n");

      const mailto = `mailto:director@redsbd.com?subject=${encodeURIComponent(
        subject.value.trim() || "REDS website enquiry"
      )}&body=${encodeURIComponent(body)}`;

      window.location.href = mailto;
      form.reset();
    });
  }

  /* GSAP animations */
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduceMotion || typeof gsap === "undefined") {
    document.querySelectorAll(".reveal").forEach((el) => {
      el.style.opacity = "1";
      el.style.transform = "none";
    });
    return;
  }

  if (typeof ScrollTrigger !== "undefined") {
    gsap.registerPlugin(ScrollTrigger);
  }

  gsap.defaults({ ease: "power3.out", duration: 0.85 });

  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    gsap.utils.toArray(".reveal").forEach((el) => {
      gsap.from(el, {
        opacity: 0,
        y: 36,
        duration: 0.9,
        scrollTrigger: {
          trigger: el,
          start: "top 88%",
          toggleActions: "play none none none",
        },
      });
    });

    gsap.utils.toArray(".reveal-stagger").forEach((group) => {
      const items = group.querySelectorAll(":scope > *");
      gsap.from(items, {
        opacity: 0,
        y: 40,
        duration: 0.75,
        stagger: 0.08,
        scrollTrigger: {
          trigger: group,
          start: "top 85%",
          toggleActions: "play none none none",
        },
      });
    });

    const heroCaption = document.querySelector(".hero-caption");
    if (heroCaption) {
      gsap.from(heroCaption, {
        opacity: 0,
        y: 24,
        duration: 1,
        delay: 0.25,
      });
    }

    const welcome = document.querySelector(".welcome-block");
    if (welcome) {
      gsap.from(welcome.children, {
        opacity: 0,
        y: 28,
        stagger: 0.12,
        duration: 0.9,
        delay: 0.1,
      });
    }
  });
})();
