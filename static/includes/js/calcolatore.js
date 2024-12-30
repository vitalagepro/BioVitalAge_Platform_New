/*  -----------------------------------------------------------------------------------------------
  Slider Range
--------------------------------------------------------------------------------------------------- */
document.querySelectorAll('input[type="range"]').forEach((slider) => {
  slider.addEventListener("input", function () {
    const value = ((this.value - this.min) / (this.max - this.min)) * 100;
    this.style.setProperty("--value", `${value}%`);
  });
});

/*  -----------------------------------------------------------------------------------------------
  User Modal log out
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
