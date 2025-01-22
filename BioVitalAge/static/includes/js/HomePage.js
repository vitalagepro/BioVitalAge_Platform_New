/*  -----------------------------------------------------------------------------------------------
  Disclaimer
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const disclaimerContainer = document.getElementById("disclaimerContainer");
  const overlay = document.getElementById("cookieOverlay");
  const initialMessage = document.getElementById("initialMessage");
  const customizeSection = document.getElementById("customizeSection");
  const disclaimerAccepted = document.cookie.includes("disclaimer_accepted=true");

  // Mostra il disclaimer se non è stato ancora accettato
  if (!disclaimerAccepted && disclaimerContainer) {
    showDisclaimer();
  }

  // Accetta tutti i cookie
  document.getElementById("acceptCookies").addEventListener("click", function () {
    sendCookieSettings({ functional: true, analytics: true, marketing: true });
    closeDisclaimer();
  });

  // Rifiuta tutti i cookie
  document.getElementById("rejectCookies").addEventListener("click", function () {
    sendCookieSettings({ functional: false, analytics: false, marketing: false });
    closeDisclaimer();
  });

  // Mostra la sezione di personalizzazione
  document.getElementById("customizeCookies").addEventListener("click", function () {
    initialMessage.classList.add("hidden-disclaimer");
    customizeSection.classList.remove("hidden-disclaimer");
  });

  // Salva le impostazioni personalizzate
  document.getElementById("saveCookies").addEventListener("click", function () {
    const functional = document.getElementById("functionalCookies").checked;
    const analytics = document.getElementById("analyticsCookies").checked;
    const marketing = document.getElementById("marketingCookies").checked;

    sendCookieSettings({ functional, analytics, marketing });
    closeDisclaimer();
  });

  // Mostra il disclaimer
  function showDisclaimer() {
    disclaimerContainer.classList.add("visible-disclaimer");
    overlay.classList.add("visible-disclaimer");
    disclaimerContainer.classList.remove("hidden-disclaimer");
    overlay.classList.remove("hidden-disclaimer");
    document.body.style.overflow = "hidden";
  }

  // Nascondi il disclaimer
  function closeDisclaimer() {
    disclaimerContainer.classList.remove("visible-disclaimer");
    overlay.classList.remove("visible-disclaimer");
    document.body.style.overflow = "auto";
    document.cookie = "disclaimer_accepted=true; path=/; max-age=31536000"; // 1 anno
  }

  // Invia le impostazioni dei cookie al server
  function sendCookieSettings(settings) {
    fetch("/accept-disclaimer/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(settings),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Errore durante il salvataggio dei cookie");
        return response.json();
      })
      .then((data) => console.log("Impostazioni salvate:", data))
      .catch((error) => console.error("Errore:", error));
  }

  // Ottieni un cookie per nome
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split("; ");
      for (let cookie of cookies) {
        if (cookie.startsWith(name + "=")) {
          cookieValue = cookie.split("=")[1];
          break;
        }
      }
    }
    return cookieValue;
  }
});

/*  -----------------------------------------------------------------------------------------------
  Modal User
--------------------------------------------------------------------------------------------------- */
const userImg = document.getElementById("userImg");
const userModal = document.getElementById("userModal");
const userModalBtn = document.getElementById("nav-bar-user-modal-btn");

function showModal() {
  userModal.classList.add("show");
}

userImg.addEventListener("mouseover", showModal);

userModal.addEventListener("mouseout", () => {
  userModal.classList.remove("show");
});

userModalBtn.addEventListener("mouseover", showModal);

function goToPatientsPage() {
  alert("Vai alla pagina di tutti i pazienti");
}
function goToRefertiPage() {
  alert("Vai alla pagina dei referti dei pazienti");
}

/*  -----------------------------------------------------------------------------------------------
  JS SIDEBAR
--------------------------------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  const sidebarTitle = document.getElementById("sidebar-title");
  const sidebarContent = document.getElementById("sidebar-content");
  const closeSidebar = document.getElementById("closeSidebar");
  const bgSidebar = document.querySelector(".bg-sidebar");

  // Gestisci il click sulle icone
  document.querySelectorAll(".sidebar-trigger").forEach((trigger) => {
    trigger.addEventListener("click", (event) => {
      event.preventDefault();
      const section = trigger.getAttribute("data-section");

      // Aggiorna contenuto della sidebar in base alla sezione
      sidebarTitle.textContent = section;
      switch (section) {
        case "Notifiche":
          sidebarContent.innerHTML = `
            <div id="notification-list">
              <h3 class="title-notice">Ultime Novità</h3>
              <a href="#" class="blog-link" title="View Blog">
                <div class="blog-container">
                  <div class="container_img">
                    <img
                      src="../../static/includes/images/search-patients-item.webp"
                      alt="img-blog"
                    />
                  </div>
                  <div>
                    <h3 class="blog-title">Blog 1</h3>
                    <p class="blog-text">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Adipisci at veniam eum quo alias suscipit corrupti,
                      commodi eveniet porro nulla magni a ipsum voluptate, totam
                      rerum? Ducimus ipsum quibusdam quam.
                    </p>
                  </div>
                </div>
              </a>
              <a href="#" class="blog-link" title="View Blog">
                <div class="blog-container">
                  <div class="container_img">
                    <img
                      src="../../static/includes/images/search-patients-item.webp"
                      alt="img-blog"
                    />
                  </div>
                  <div>
                    <h3 class="blog-title">Blog 2</h3>
                    <p class="blog-text">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Adipisci at veniam eum quo alias suscipit corrupti,
                      commodi eveniet porro nulla magni a ipsum voluptate, totam
                      rerum? Ducimus ipsum quibusdam quam.
                    </p>
                  </div>
                </div>
              </a>
              <a href="#" class="blog-link" title="View Blog">
                <div class="blog-container">
                  <div class="container_img">
                    <img
                      src="../../static/includes/images/search-patients-item.webp"
                      alt="img-blog"
                    />
                  </div>
                  <div>
                    <h3 class="blog-title">Blog 3</h3>
                    <p class="blog-text">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Adipisci at veniam eum quo alias suscipit corrupti,
                      commodi eveniet porro nulla magni a ipsum voluptate, totam
                      rerum? Ducimus ipsum quibusdam quam.
                    </p>
                  </div>
                </div>
              </a>
              <h3 class="title-notice">Altre Novità</h3>
              <a href="#" class="blog-link" title="View Blog">
                <div class="blog-container">
                  <div class="container_img">
                    <img
                      src="../../static/includes/images/search-patients-item.webp"
                      alt="img-blog"
                    />
                  </div>
                  <div>
                    <h3 class="blog-title">Blog 1</h3>
                    <p class="blog-text">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Adipisci at veniam eum quo alias suscipit corrupti,
                      commodi eveniet porro nulla magni a ipsum voluptate, totam
                      rerum? Ducimus ipsum quibusdam quam.
                    </p>
                  </div>
                </div>
              </a>
              <a href="#" class="blog-link" title="View Blog">
                <div class="blog-container">
                  <div class="container_img">
                    <img
                      src="../../static/includes/images/search-patients-item.webp"
                      alt="img-blog"
                    />
                  </div>
                  <div>
                    <h3 class="blog-title">Blog 2</h3>
                    <p class="blog-text">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Adipisci at veniam eum quo alias suscipit corrupti,
                      commodi eveniet porro nulla magni a ipsum voluptate, totam
                      rerum? Ducimus ipsum quibusdam quam.
                    </p>
                  </div>
                </div>
              </a>
              <a href="#" class="blog-link" title="View Blog">
                <div class="blog-container">
                  <div class="container_img">
                    <img
                      src="../../static/includes/images/search-patients-item.webp"
                      alt="img-blog"
                    />
                  </div>
                  <div>
                    <h3 class="blog-title">Blog 3</h3>
                    <p class="blog-text">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Adipisci at veniam eum quo alias suscipit corrupti,
                      commodi eveniet porro nulla magni a ipsum voluptate, totam
                      rerum? Ducimus ipsum quibusdam quam.
                    </p>
                  </div>
                </div>
              </a>
              <a href="#" class="blog-link" title="View Blog">
                <div class="blog-container">
                  <div class="container_img">
                    <img
                      src="../../static/includes/images/search-patients-item.webp"
                      alt="img-blog"
                    />
                  </div>
                  <div>
                    <h3 class="blog-title">Blog 1</h3>
                    <p class="blog-text">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Adipisci at veniam eum quo alias suscipit corrupti,
                      commodi eveniet porro nulla magni a ipsum voluptate, totam
                      rerum? Ducimus ipsum quibusdam quam.
                    </p>
                  </div>
                </div>
              </a>
              <a href="#" class="blog-link" title="View Blog">
                <div class="blog-container">
                  <div class="container_img">
                    <img
                      src="../../static/includes/images/search-patients-item.webp"
                      alt="img-blog"
                    />
                  </div>
                  <div>
                    <h3 class="blog-title">Blog 2</h3>
                    <p class="blog-text">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Adipisci at veniam eum quo alias suscipit corrupti,
                      commodi eveniet porro nulla magni a ipsum voluptate, totam
                      rerum? Ducimus ipsum quibusdam quam.
                    </p>
                  </div>
                </div>
              </a>
              <a href="#" class="blog-link" title="View Blog">
                <div class="blog-container">
                  <div class="container_img">
                    <img
                      src="../../static/includes/images/search-patients-item.webp"
                      alt="img-blog"
                    />
                  </div>
                  <div>
                    <h3 class="blog-title">Blog 3</h3>
                    <p class="blog-text">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Adipisci at veniam eum quo alias suscipit corrupti,
                      commodi eveniet porro nulla magni a ipsum voluptate, totam
                      rerum? Ducimus ipsum quibusdam quam.
                    </p>
                  </div>
                </div>
              </a>
              <a href="#" class="blog-link" title="View Blog">
                <div class="blog-container">
                  <div class="container_img">
                    <img
                      src="../../static/includes/images/search-patients-item.webp"
                      alt="img-blog"
                    />
                  </div>
                  <div>
                    <h3 class="blog-title">Blog 1</h3>
                    <p class="blog-text">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Adipisci at veniam eum quo alias suscipit corrupti,
                      commodi eveniet porro nulla magni a ipsum voluptate, totam
                      rerum? Ducimus ipsum quibusdam quam.
                    </p>
                  </div>
                </div>
              </a>
              <a href="#" class="blog-link" title="View Blog">
                <div class="blog-container">
                  <div class="container_img">
                    <img
                      src="../../static/includes/images/search-patients-item.webp"
                      alt="img-blog"
                    />
                  </div>
                  <div>
                    <h3 class="blog-title">Blog 2</h3>
                    <p class="blog-text">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Adipisci at veniam eum quo alias suscipit corrupti,
                      commodi eveniet porro nulla magni a ipsum voluptate, totam
                      rerum? Ducimus ipsum quibusdam quam.
                    </p>
                  </div>
                </div>
              </a>
              <a href="#" class="blog-link" title="View Blog">
                <div class="blog-container">
                  <div class="container_img">
                    <img
                      src="../../static/includes/images/search-patients-item.webp"
                      alt="img-blog"
                    />
                  </div>
                  <div>
                    <h3 class="blog-title">Blog 3</h3>
                    <p class="blog-text">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Adipisci at veniam eum quo alias suscipit corrupti,
                      commodi eveniet porro nulla magni a ipsum voluptate, totam
                      rerum? Ducimus ipsum quibusdam quam.
                    </p>
                  </div>
                </div>
              </a>
            </div>
            `;
          break;
        case "Email":
          sidebarContent.innerHTML = "<p>Qui trovi tutte le email.</p>";
          break;
        case "Update":
          sidebarContent.innerHTML = "<p>Qui trovi gli aggiornamenti.</p>";
          break;
        default:
          sidebarContent.innerHTML = "<p>Contenuto non disponibile.</p>";
      }

      // Mostra la sidebar
      document.body.classList.add("visible");
    });
  });

  // Chiudi la sidebar
  bgSidebar.addEventListener("click", () => {
    document.body.classList.remove("visible");
  });

  closeSidebar.addEventListener("click", () => {
    document.body.classList.remove("visible");
  });
});
