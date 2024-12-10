const ContainerIndicatori = document.querySelectorAll('.indicator-container')

ContainerIndicatori.forEach(element => {

    const indicatorContainer = element.querySelector('.indicator-content-container');
    const containerRangePositive = indicatorContainer.querySelector('.positiveTesto');

    if(!containerRangePositive){
        return
    }
    const rangePositiveIndicator = containerRangePositive.querySelectorAll('p');
    const indicator = element.querySelector('.indicatore');

    let valoreEsame = indicator.getAttribute('data-value');
    let minPositive = rangePositiveIndicator[0].textContent;
    let maxPositive = rangePositiveIndicator[1].textContent;

    let rangeNegativeIndicator = element.querySelector('.negativeTesto').textContent.split(" ")[0];
    let extremeRightRangeIndicator = element.querySelector('.extremeNegativeRange').textContent.split(" ")[1]; 
    
 
    if(parseFloat(valoreEsame) <= parseFloat(minPositive) && parseFloat(valoreEsame) >= parseFloat(maxPositive)){
        
        if(parseFloat(valoreEsame) == parseFloat(minPositive)){
            indicator.style.left = "28%";
        }
        else if(parseFloat(valoreEsame) == parseFloat(maxPositive)){
            indicator.style.left = "58%";
        }
        else{
            const percentuale = ((minPositive - valoreEsame) / (minPositive - maxPositive)) * 40;
            let fixedPercentuale = percentuale + 26;
            indicator.style.left = `${Math.round(fixedPercentuale)}%`;
        }
    }
    else{
        if(parseFloat(valoreEsame) > parseFloat(minPositive)){

            if(parseFloat(valoreEsame) > parseFloat(rangeNegativeIndicator)){
                indicator.style.left = "-3%";
            }
            else{
                const percentuale = ((rangeNegativeIndicator - valoreEsame) / (rangeNegativeIndicator - minPositive)) * 30;
                let fixedPercentuale = Math.round(percentuale) - 4;
                indicator.style.left = `${fixedPercentuale}%`;
            }
        }

        else{
            if(parseFloat(valoreEsame) < parseFloat(extremeRightRangeIndicator)){
                indicator.style.left = "95%";
            }
            else{
                const percentuale = ((maxPositive - valoreEsame) / (maxPositive - extremeRightRangeIndicator)) * 30;
                let fixedPercentuale = percentuale + 66;
                indicator.style.left = `${fixedPercentuale}%`;
            }
        }
    } 
});
