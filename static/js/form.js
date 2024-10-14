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

// Form submission handling
document.getElementById('stress-analysis-form').addEventListener('submit', function(event) {
    event.preventDefault();  
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
