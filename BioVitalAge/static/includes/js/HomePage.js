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
  const sidebar = document.querySelectorAll("#sidebar");
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
