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

  /* Contact form — FormSubmit (no backend) */
  if (form) {
    const status = document.querySelector("#form-status");
    const submitBtn = form.querySelector('[type="submit"]');
    const endpoint =
      form.getAttribute("action") ||
      "https://formsubmit.co/ajax/rahmanamanur51@gmail.com";

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const name = form.querySelector('[name="name"]');
      const email = form.querySelector('[name="email"]');
      const subject = form.querySelector('[name="subject"]');
      const message = form.querySelector('[name="message"]');
      const subjectHidden = form.querySelector('[name="_subject"]');

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

      if (subjectHidden) {
        subjectHidden.value = subject.value.trim() || "REDS website enquiry";
      }

      if (status) {
        status.classList.remove("is-error");
        status.textContent = "Sending…";
      }
      if (submitBtn) submitBtn.disabled = true;

      try {
        const res = await fetch(endpoint, {
          method: "POST",
          headers: {
            Accept: "application/json",
          },
          body: new FormData(form),
        });

        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
          throw new Error(data.message || "Unable to send message.");
        }

        if (status) {
          status.classList.remove("is-error");
          status.textContent = "Thank you. Your message has been sent.";
        }
        form.reset();
        if (subjectHidden) subjectHidden.value = "REDS website enquiry";
      } catch (err) {
        if (status) {
          status.classList.add("is-error");
          status.textContent =
            err && err.message
              ? err.message
              : "Something went wrong. Please try again or email us directly.";
        }
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }

  /* GSAP animations */
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function showReveals() {
    document.querySelectorAll(".reveal, .reveal-stagger > *").forEach((el) => {
      el.style.opacity = "1";
      el.style.transform = "none";
    });
  }

  if (reduceMotion || typeof gsap === "undefined") {
    showReveals();
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
        clearProps: "transform",
        scrollTrigger: {
          trigger: el,
          start: "top 90%",
          toggleActions: "play none none none",
          once: true,
        },
      });
    });

    gsap.utils.toArray(".reveal-stagger").forEach((group) => {
      const items = group.querySelectorAll(":scope > *");
      gsap.from(items, {
        opacity: 0,
        y: 28,
        duration: 0.7,
        stagger: 0.06,
        clearProps: "transform",
        scrollTrigger: {
          trigger: group,
          start: "top 92%",
          toggleActions: "play none none none",
          once: true,
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
        clearProps: "transform",
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
        clearProps: "transform",
      });
    }

    window.addEventListener("load", () => {
      if (typeof ScrollTrigger !== "undefined") {
        ScrollTrigger.refresh();
      }
    });
  });
})();
