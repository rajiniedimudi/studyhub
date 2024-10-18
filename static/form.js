console.log("check");
window.scrollTo({ top: 0, behavior: 'smooth' });
function showLoading() {
    console.log("clicked");
    window.scrollTo({ top: 0, behavior: 'smooth' });
    document.getElementById("loading-overlay").style.display = "flex";
    document.querySelector(".full-container").classList.add("faded");
}

function hideLoading() {
    document.getElementById("loading-overlay").style.display = "none";
    document.querySelector(".full-container").classList.remove("faded");
}

let formValid = true; // Initialize formValid

// Form submission handling
document.getElementById('stress-analysis-form').addEventListener('submit', function(event) {
    event.preventDefault();  
    console.log(stressValid , copyValid , wellValid);
    formValid = stressValid && copyValid && wellValid;

    if (formValid){
        showLoading();  
        const form = event.target;
        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // setTimeout(() => {
            hideLoading();  
            document.getElementsByClassName("form-container")[0].style.display = "none";
            const resultContainer = document.getElementById('result-container');
            resultContainer.style.display = "flex";
            resultContainer.style.justifyContent = 'center';
            resultContainer.style.alignItems = 'center';
            resultContainer.style.flexDirection = 'column';
            const resultTips = document.getElementById('result-tips');
            resultTips.innerHTML = ''; 
            resultTips.style.color = "#343a40";
            resultTips.style.listStyle = "none";

            const tips = data.result.match(/\d\.\s.*?(?=\n|$)/g);
            if (tips) {
                tips.forEach(tip => {
                    const li = document.createElement('li');
                    li.style.padding = "15px 120px";
                    li.style.fontSize = "18px";
                    li.textContent = tip.trim();
                    resultTips.appendChild(li);
                });
                const stressLevel = parseInt(document.getElementById("stress-level").value);
                const copingMechanisms = parseInt(document.getElementById("coping-mechanisms").value);
                const wellBeing = parseInt(document.getElementById("well-being").value);
                const stress_precent = document.getElementById('stress-level-percentage');
                const totalScore = stressLevel + copingMechanisms + wellBeing;
                const stressManagementPercentage = (totalScore / 9) * 100;
                stress_precent.innerHTML = `Your stress management percentage is: ${stressManagementPercentage.toFixed(2)}%`;

                stress_precent.style.fontSize = "20px";
                stress_precent.style.border = "#fb6977";
                stress_precent.style.padding = "10px";
                stress_precent.style.backgroundColor = "#fb6977";
                stress_precent.style.borderRadius = "15px";
                stress_precent.style.color = "#fbe3e3";
            } else {
                const li = document.createElement('li');
                li.style.padding = "15px 120px";
                li.style.fontSize = "18px";
                li.textContent = "No tips found. Please check your input.";
                resultTips.appendChild(li);
            }
        // }, 10000);  
        })
        .catch(error => {
            console.error('Error:', error);
            hideLoading();  
        });
    }else{
        alert("form not valid");
    }
});


// Diet changes
function handleDietChange() {
    const dietSelect = document.getElementById('diet-type');
    const otherInput = document.getElementById('diet-type-other');
    if (dietSelect.value === 'other') {
        otherInput.disabled = false;
        otherInput.style.cursor = 'text';
    } else {
        otherInput.disabled = true;
        otherInput.style.cursor = 'not-allowed';
        otherInput.value = '';  
    }
}

// Emotional changes
function handleEmotionalChange() {
    const emotionalSelect = document.getElementById('emotional-state');
    const otherTextInput = document.getElementById('other-emotional-state-text');

    if (emotionalSelect.value === 'other-emotional-state') {
        otherTextInput.disabled = false;
        otherTextInput.style.cursor = 'text';
    } else {
        otherTextInput.disabled = true;
        otherTextInput.style.cursor = 'not-allowed';
        otherTextInput.value = '';  
    }
}

function handleStressLevel() {
    stress_level = document.getElementById("stress-level").value;
    let stressError = document.getElementsByClassName("stress-error-msg")[0];
    if (parseInt(stress_level)>10 || parseInt(stress_level<1)){
        console.log(stressError, 'docc')
        stressError.style.fontSize = "15px";
        stressError.style.color = "red";
        stressError.innerHTML = "Enter valid number (1-10)";
        stressValid = false;
    }else{
        stressValid = true;
        stressError.innerHTML = "";
    }
   
}

function handleCopyLevel() {
    copying_mech = document.getElementById("coping-mechanisms").value;
    let copyError = document.getElementsByClassName("copy-error-msg")[0];
    if (parseInt(copying_mech)>10 || parseInt(copying_mech<1)){
        console.log(copyError, 'copy')
        copyError.style.fontSize = "15px";
        copyError.style.color = "red";
        copyError.innerHTML = "Enter valid number (1-10)";
        copyValid = false;
    }else{
        copyValid = true;
        copyError.innerHTML = "";
    }
}


function handleWellLevel() {
    wellBeing = document.getElementById("well-being").value;
    let wellError = document.getElementsByClassName("well-error-msg")[0];
    if (parseInt(wellBeing)>10 || parseInt(wellBeing<1)){
        console.log(wellBeing, 'copy')
        wellError.style.fontSize = "15px";
        wellError.style.color = "red";
        wellError.innerHTML = "Enter valid number (1-10)";
        wellValid = false;
    }else{
        wellValid = true;
        wellError.innerHTML = "";
    }
}