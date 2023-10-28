document.documentElement.style.setProperty(
    '--nav-height',
    document.getElementById("navbar").offsetHeight
);

function addListeners() {
    "use strict";
    const legendTips = {
        "MHHW": "Mean Higher High Water",
        "EWL1R": "Extreme Water Level 1-year Return",
        "EWL2R": "Extreme Water Level 2-year Return",
        "EWL10R": "Extreme Water Level 10-year Return",
        "NFHL100": "FEMA 100-year Flood",
        "CAT1": "Category-1 Hurricane",
        "CAT3": "Category-3 Hurricane",
        "CAT5": "Category-5 Hurricane"
    };
    const legendPopup = (item) => {
        item.addEventListener('mouseover', (event) => {
            // Get the element that triggered the event
            const hoveredElement = event.target;
            const parentElement = hoveredElement.parentNode;

            const popup = document.createElement('div');
            popup.setAttribute('id', 'legend_popup');
            popup.textContent = legendTips[parentElement.children[0].innerHTML];
            popup.classList.add('popup');

            const parentPos = parentElement.getBoundingClientRect();
            const popupMessageTop = parentPos.top - 10;
            const popupMessageLeft = parentPos.left + parentPos.width + 5;
            popup.style.top = `${popupMessageTop}px`;
            popup.style.left = `${popupMessageLeft}px`;
            document.body.appendChild(popup);
        });

        item.addEventListener("mouseout", () => {
            const popup = document.getElementById("legend_popup");
            document.body.removeChild(popup);
        });
    };
    const sliderPopup = (item) => {
        item.addEventListener('mouseover', (event) => {
            // Get the element that triggered the event
            const hoveredElement = event.target;

            const popup = document.createElement('div');
            popup.setAttribute('id', 'slider_popup');
            popup.textContent = legendTips[hoveredElement.innerHTML];
            popup.classList.add('popup');

            const popup_hidden_span = document.createElement('span');
            popup_hidden_span.style.visibility = "hidden";
            popup_hidden_span.innerHTML = popup.textContent;
            document.body.appendChild(popup_hidden_span);

            const hoveredPos = hoveredElement.getBoundingClientRect();
            const popupMessageTop = hoveredPos.top - 10;
            const popupMessageLeft = hoveredPos.left - hoveredPos.width - popup_hidden_span.offsetWidth;
            document.body.removeChild(popup_hidden_span);

            popup.style.top = `${popupMessageTop}px`;
            popup.style.left = `${popupMessageLeft}px`;
            document.body.appendChild(popup);
        });

        item.addEventListener("mouseout", () => {
            const popup = document.getElementById("slider_popup");
            document.body.removeChild(popup);
        });
    };

    const lineChart = document.getElementById("line-chart");
    const legendItems = lineChart.getElementsByClassName("traces");

    for (let i = 0; i < legendItems.length; i++) {
        legendPopup(legendItems[i]);
    }

    const ySlider = document.getElementById("map-y-slider");
    const marks = ySlider.getElementsByClassName("rc-slider-mark-text");

    for (let i = 0; i < marks.length; i++) {
        sliderPopup(marks[i]);
    }
};

function createIntroTour() {
    const introTour = new Shepherd.Tour({
        useModalOverlay: true,
        defaultStepOptions: {
            classes: 'shepherd-theme-arrows',
            cancelIcon: {
                enabled: true
            }
        }
    });

    introTour.addStep({
        id: 'step1',
        title: 'Welcome to the Flood Risk Viewer!',
        text: 'This tool' +
            ' allows you to explore the impacts of sea level rise' +
            ' and storm surge on the City of Cedar Key.' +
            ' Click "Next" to continue.',
        buttons: [
            {
                text: 'Next',
                action: introTour.next
            }
        ],
    });

    introTour.addStep({
        id: 'step2',
        title: 'Flood Risk by Asset Types',
        text: 'Click these buttons to view potential flood depths' +
            ' for a specific asset type.' +
            ' The "Get Started" button on the welcome page directs' +
            ' to <strong>HOUSING</strong> by default.',
        attachTo: {
            element: '#navbar-links-group',
            on: 'bottom',
        },
        buttons: [
            {
                text: 'Next',
                action: introTour.next
            }
        ],
        floatingUIOptions: {
            middleware: [window.FloatingUIDOM.offset({mainAxis: 20})]
        }
    });

    introTour.addStep({
        id: 'step3',
        title: 'Pick a Scenario',
        text: 'Choose a specifc scenario by dragging' +
            ' the slider. <strong>Hover</strong> on an acronym to' +
            ' see its full name.',
        attachTo: {
            element: '#map-y-slider',
            on: 'left',
        },
        buttons: [
            {
                text: 'Next',
                action: introTour.next
            }
        ],
        floatingUIOptions: {
            middleware: [window.FloatingUIDOM.offset({mainAxis: 20})]
        }
    });

    introTour.addStep({
        id: 'step4',
        title: 'Pick a Year',
        text: 'Choose a year to see specific scenario you selected' +
            ' under that year. The default year is 2040.',
        attachTo: {
            element: '#map-x-slider',
            on: 'top',
        },
        buttons: [
            {
                text: 'Next',
                action: introTour.next
            }
        ],
        floatingUIOptions: {
            middleware: [window.FloatingUIDOM.offset({mainAxis: 20})]
        }
    });

    introTour.addStep({
        id: 'step5',
        title: 'Overview, Challenges, and Value',
        text: 'Learn about the types of structures and assets analyzed ' +
            ' in Cedar Key, and the challenges facing the city.' +
            ' Also, read about the values that will guide the city’s ' +
            ' resilience and flood risk reduction strategies.' +
            ' <strong>Scroll-down</strong> to read more.',
        attachTo: {
            element: '#intro-message',
            on: 'right',
        },
        buttons: [
            {
                text: 'Next',
                action: introTour.next
            }
        ],
        floatingUIOptions: {
            middleware: [window.FloatingUIDOM.offset({mainAxis: 20})]
        }
    });

    introTour.addStep({
        id: 'step6',
        title: 'Percent of Inundated Assets',
        text: 'This chart provides an overview of the percentage of' +
            ' inundated assets with the specific asset type is currently' +
            ' under selection. Each line represents a specific (storm) scenario,' +
            ' which follows the same acronyms as the vertical slider before.' +
            ' <strong>Hover</strong> on a data point (any combination of year and scenario)' +
            ' to see its value.' +
            ' <strong>Single-click</strong> on a legend item to hide a scenario.' +
            ' <strong>Double-click</strong> to show just that scenario.',
        attachTo: {
            element: '#line-chart',
            on: 'right',
        },
        buttons: [
            {
                text: 'Next',
                action: introTour.next
            }
        ],
        floatingUIOptions: {
            middleware: [window.FloatingUIDOM.offset({mainAxis: 20})]
        }
    });

    introTour.addStep({
        id: 'step7',
        title: 'Flood Depth Classification',
        text: 'This chart is in sync with the chart above.' +
            ' When you <strong>Hover</strong> on a particular data point' +
            ' above, it shows the percent of all the inundated assets' +
            ' by flood depths divided into 6 classes.',
        attachTo: {
            element: '#bar-chart',
            on: 'right',
        },
        buttons: [
            {
                text: 'FINISH',
                action: introTour.next
            }
        ],
        floatingUIOptions: {
            middleware: [window.FloatingUIDOM.offset({mainAxis: 20})]
        }
    });

    if (window.location.href.includes('viewer/housing')) {
        // Initiate the tour
        // introTour.start();
        if(!sessionStorage.getItem('shepherd-tour')) {
            introTour.start();
            sessionStorage.setItem('shepherd-tour', 'yes');
        }
    }
}