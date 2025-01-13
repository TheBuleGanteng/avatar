// This is a collection of JS utility functions used in other JS files



// Pulls the CSRF token and exports it, making it available for other JS files to pull
let csrfToken = '';
let csrfMeta = document.querySelector('meta[name="csrf-token"]');
if (csrfMeta) {
    csrfToken = csrfMeta.content;
    console.log(`running aichat.js ... CSRF Token set: ${ csrfToken }`);
} else {
    console.log(`running aichat.js ... CSRF meta tag not found.`);
}
export { csrfToken };



//------------------------------------------------------------------------------



// Debounce function takes two arguments: function to be debounced and time (with default in ms)
export function debounce(func, timeout) { // Default timeout set to 300ms
    let timer;
    return function(...args) {
        const context = this; // Capture the current context
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(context, args), timeout);
    };
}



//------------------------------------------------------------------------------



// Triggers aichat_chat generate_embeddings, which generates the embeddings and retriever
export function generateEmbeddings() {
    console.log(`running utils.js ... running generateEmbeddings()`);

    const generateEmbeddingsUrl = '/aichat/generate_embeddings/';
    
    return fetch(generateEmbeddingsUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                console.error(`running utils.js ... Server responded with status: ${response.status}`);
                console.error(`running utils.js ... Response text: ${text}`);
                throw new Error(`HTTP error! status: ${response.status}`);
            });
        }
        return response.json();
    })
    .catch(error => {
        console.error(`running utils.js ... error during AJAX request: ${error}`);
        throw error;
    });
}



//------------------------------------------------------------------------------



// Submits various forms via Ajax, which allows for form submission without page reload
export function handleAjaxFormSubmission(url, formData) {
    return fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
    })
    .then(response => {
        // Attempt to parse the response as JSON regardless of the status
        return response.json().then(data => {
            if (!response.ok) {
                console.error(`running utils.js ... Server responded with status: ${response.status}`);
                console.error(`running utils.js ... Response text: ${text}`);
                throw new Error(`HTTP error! status: ${response.status}`);
            };
            return data;
        });
    })
    .catch(error => {
        console.error(`running utils.js ... error during AJAX request: ${error}`);
        throw error;
    });
}



//------------------------------------------------------------------------------



// Scroll to the bottom of feedDiv
export function jsScrollDown() {
    // Scroll to the bottom of the page
    window.scrollTo(0, document.body.scrollHeight);
}



//------------------------------------------------------------------------------



// Format number with commas
export function toNumberWithCommas(number) {
    return Number(number).toLocaleString();
}



//------------------------------------------------------------------------------



// Convert a decimal to a percentage
export function toPercentage(value) {
    return (value * 100).toFixed(0) + '%';
}



//------------------------------------------------------------------------------



// Collapse accordion 1, expand accordion 2
export function transitionAccordionOneToTwo() {
    const accordion1Element = document.getElementById('panelsStayOpen-collapseOne');
    const accordion2Element = document.getElementById('panelsStayOpen-collapseTwo');

    // Ensure that both elements exist in the DOM before proceeding
    if (accordion1Element && accordion2Element) {
        var accordion1 = new bootstrap.Collapse(accordion1Element, { toggle: false });
        var accordion2 = new bootstrap.Collapse(accordion2Element, { toggle: false });

        accordion1.hide(); // Collapse the first accordion
        accordion2.show(); // Show the second accordion
        console.log(`running transitionAccordionOneToTwo() ... collapsed accordion1 and expanded accordion2`);
    } else {
        console.log(`running transitionAccordionOneToTwo() ... accordion1 and/or accordion2 not present in the DOM. Unable to run transitionAccordionOneToTwo()`);
    }
}



//------------------------------------------------------------------------------



// Collapse accordion 2, expand accordion 1
export function transitionAccordionTwoToOne() {
    
    const accordion1Element = document.getElementById('panelsStayOpen-collapseOne');
    const accordion2Element = document.getElementById('panelsStayOpen-collapseTwo');

    // Ensure that both elements exist in the DOM before proceeding
    if (accordion1Element && accordion2Element) {

        var accordion1 = new bootstrap.Collapse(accordion1Element, { toggle: false });
        var accordion2 = new bootstrap.Collapse(accordion2Element, { toggle: false });

        accordion2.hide(); // Collapse the first accordion
        accordion1.show(); // Show the second accordion
    } else {
        console.log(`running transitionAccordionTwoTpOne() ... accordion1 and/or accordion2 not present in the DOM. Unable to run transitionAccordionTwoToOne()`)

    }

}



//------------------------------------------------------------------------------



// Collapse accordion 2, expand accordion 3
export function transitionAccordionTwoToThree() {
    
    // If DB updated successfully, hide accordion 1, expand accordion 2
    var accordion2Element = document.getElementById('panelsStayOpen-collapseTwo')
    var accordion3Element = document.getElementById('panelsStayOpen-collapseThree')

    if (accordion2Element && accordion3Element) {
        var accordion2 = new bootstrap.Collapse(accordion2Element, { toggle: false });
        var accordion3 = new bootstrap.Collapse(accordion3Element, { toggle: false });

        accordion2.hide(); // Collapse the first accordion
        accordion3.show(); // Show the second accordion
    } else {
        console.log(`running transitionAccordionTwoToThree() ... accordion2 and/or accordion3 not present in the DOM. Unable to run transitionAccordionTwoToThree()`)
    }

}



//------------------------------------------------------------------------------



// Update the profileForm for the field submitted
export function updateProfileForm(fieldName, fieldValue) {

    // Prepare data to send in the request
    const formData = new FormData();

    formData.append('field', fieldName);  // Use the field name from the input
    formData.append('value', fieldValue);  // Use the field value from the input

    const updateProfileUrl = '/aichat/update_profile/';
    console.log(`running updateUserProfile.js ... updateProfileUrl is: ${ updateProfileUrl }`);

    handleAjaxFormSubmission(updateProfileUrl, formData)
    .then(data => {
        if (data.status === 'success') {
            console.log('running updateUserProfile.js ... profile updated successfully');

        } else {
            console.error(`running updateUserProfile.js ... error submitting form: ${ data.errors}`);
            alert('Failed to update profile');
        }
    })
    .catch(error => {
        console.error(`running setRagSourcesUsed() ... error during form submission: ${ error}`);
        alert('An unexpected error occurred.');
    });
};

