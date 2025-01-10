/*  -----------------------------------------------------------------------------------------------
Function for gender selection
--------------------------------------------------------------------------------------------------- */
document.getElementById("gender").addEventListener("change", function () {
  const selectedGender = this.value;

  // Seleziona TUTTI gli elementi di input all'interno dei form-group
  const formGroups = document.querySelectorAll(".form-group");

  formGroups.forEach((group) => {
    const label = group.querySelector("label");
    const numberInput = group.querySelector('input[type="number"]');
    const rangeInput = group.querySelector('input[type="range"]');

    if (label && numberInput && rangeInput) {
      const isMan = label.textContent.includes("Man");
      const isWoman = label.textContent.includes("Woman");

      // Logica di disabilitazione
      if (
        (selectedGender === "M" && isWoman) ||
        (selectedGender === "F" && isMan)
      ) {
        numberInput.disabled = true;
        rangeInput.disabled = true;
      } else {
        numberInput.disabled = false;
        rangeInput.disabled = false;
      }
    }
  });
});

const ContainerIndicatori = document.querySelectorAll(".indicator-container");

ContainerIndicatori.forEach((element) => {
  const indicatorContainer = element.querySelector(
    ".indicator-content-container"
  );
  const containerRangePositive =
    indicatorContainer.querySelector(".positiveTesto");

  if (!containerRangePositive) {
    return;
  }
  const rangePositiveIndicator = containerRangePositive.querySelectorAll("p");
  const indicator = element.querySelector(".indicatore");

  let valoreEsame = indicator.getAttribute("data-value");
  let minPositive = rangePositiveIndicator[0].textContent;
  let maxPositive = rangePositiveIndicator[1].textContent;

  let rangeNegativeIndicator = element
    .querySelector(".negativeTesto")
    .textContent.split(" ")[0];
  let extremeRightRangeIndicator = element
    .querySelector(".extremeNegativeRange")
    .textContent.split(" ")[1];

  if (
    parseFloat(valoreEsame) <= parseFloat(minPositive) &&
    parseFloat(valoreEsame) >= parseFloat(maxPositive)
  ) {
    if (parseFloat(valoreEsame) == parseFloat(minPositive)) {
      indicator.style.left = "28%";
    } else if (parseFloat(valoreEsame) == parseFloat(maxPositive)) {
      indicator.style.left = "58%";
    } else {
      const percentuale =
        ((minPositive - valoreEsame) / (minPositive - maxPositive)) * 40;
      let fixedPercentuale = percentuale + 26;
      indicator.style.left = `${Math.round(fixedPercentuale)}%`;
    }
  } else {
    if (parseFloat(valoreEsame) > parseFloat(rangeNegativeIndicator)) {
      if (parseFloat(valoreEsame) < parseFloat(rangeNegativeIndicator)) {
        indicator.style.left = "-3%";
        console.log("sono qui");
      } else {
        const percentuale =
          ((rangeNegativeIndicator - valoreEsame) /
            (rangeNegativeIndicator - minPositive)) *
          30;
        let fixedPercentuale = Math.round(percentuale) - 4;
        if (fixedPercentuale < 0) {
          fixedPercentuale = 1;
        }
        indicator.style.left = `${fixedPercentuale}%`;

        console.log(fixedPercentuale);
      }
    } else {
      if (parseFloat(valoreEsame) > parseFloat(extremeRightRangeIndicator)) {
        indicator.style.left = "95%";
      } else {
        const percentuale =
          ((maxPositive - valoreEsame) /
            (maxPositive - extremeRightRangeIndicator)) *
          30;
        let fixedPercentuale = percentuale + 66;
        indicator.style.left = `${fixedPercentuale}%`;
      }
    }
  }
});
