let data = [];

fetch("/static/js/paises.json")
    .then(response => response.json())
    .then(json => {
        data = json;
        populateCountries();
    });

const countrySelect = document.getElementById('country');
const stateSelect = document.getElementById('state');
const citySelect = document.getElementById('city');

function populateCountries() {
    data.forEach(country => {
        const option = document.createElement('option');
        option.value = country.iso2;
        option.textContent = country.name;
        countrySelect.appendChild(option);
    });
    countrySelect.disabled = false;
}

countrySelect.addEventListener('change', function () {
    const selectedCountry = data.find(country => country.iso2 === this.value);
    stateSelect.innerHTML = '<option value="">Seleccione una región</option>';
    citySelect.innerHTML = '<option value="">Seleccione una ciudad</option>';
    citySelect.disabled = true;

    if (selectedCountry && selectedCountry.states.length > 0) {
        selectedCountry.states.forEach(state => {
            const option = document.createElement('option');
            option.value = state.state_code;
            option.textContent = state.name;
            stateSelect.appendChild(option);
        });
        stateSelect.disabled = false;
    } else {
        stateSelect.disabled = true;
    }
});

stateSelect.addEventListener('change', function () {
    const selectedCountry = data.find(country => country.iso2 === countrySelect.value);
    const selectedState = selectedCountry.states.find(state => state.state_code === this.value);
    citySelect.innerHTML = '<option value="">Seleccione una ciudad</option>';

    if (selectedState && selectedState.cities.length > 0) {
        selectedState.cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city.name;
            option.textContent = city.name;
            citySelect.appendChild(option);
        });
        citySelect.disabled = false;
    } else {
        citySelect.disabled = true;
    }
});

$(function () {
    "use strict";
    $("#basicwizard").bootstrapWizard();
    $("#progressbarwizard").bootstrapWizard({
        onTabShow: function (t, r, a) {
            var o = (a + 1) / r.find("li").length * 100;
            $("#progressbarwizard").find(".bar").css({ width: o + "%" });
        }
    });
    $("#btnwizard").bootstrapWizard({
        nextSelector: ".button-next",
        previousSelector: ".button-previous",
        firstSelector: ".button-first",
        lastSelector: ".button-last"
    });
    $("#rootwizard").bootstrapWizard({
        onNext: function (t, r, a) {
            var o = $($(t).data("targetForm"));
            if (o && (o.addClass("was-validated"), !1 === o[0].checkValidity()))
                return event.preventDefault(), event.stopPropagation(), !1
        }
    })
});

document.addEventListener("DOMContentLoaded", function () {
    const nextBtn = document.getElementById("btn-next");

    nextBtn.addEventListener("click", function (e) {
        const activeTab = document.querySelector(".tab-pane.active");
        const nextTab = activeTab.nextElementSibling;

        if (!nextTab || !nextTab.classList.contains("tab-pane")) {
            document.querySelector("form").submit();
        }

        e.preventDefault();
    });
});