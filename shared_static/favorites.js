// The JS below attacheds eventListeners to the favorite star icons and adds/removes a given expert from the list of favorites accorordingly

import { csrfToken } from './utils.js';
import { showSpinner, hideSpinner } from './loadingspinner.js';

export function jsFavoriteIconMonitor() { 

    const favoriteIcons = document.getElementsByName('favorite-icon');

    if (favoriteIcons.length > 0) {
        console.log(`running favorites.js ... presence of favoriteIcons detected`);
        
        for (let j = 0; j < favoriteIcons.length; j++) {
            const icon = favoriteIcons[j];
            const iconExpertId = icon.getAttribute('data-expert-id');
            icon.addEventListener('click', function() {
                console.log(`running favorites.js ... click detected in favorite icon with expert ID ${ iconExpertId }`);
                if (icon.classList.contains('bi-star')) { // If the star isn't filled, fill it
                    icon.classList.remove('bi-star')  
                    icon.classList.add('bi-star-fill', 'yellow-star');
                }
                else { // If the star is filled, unfill it
                    icon.classList.remove('bi-star-fill', 'yellow-star');
                    icon.classList.add('bi-star')
                }
                updateFavorite(iconExpertId);

                // If the path includes "favorites", then reload page
                if (window.location.pathname.includes('/favorites/')) {
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000); // 0.5-second delay
                }    
            });
        };
    };
};

// Function to update the database
function updateFavorite(iconExpertId) {
    showSpinner(); // Show the spinner

    fetch('/avatar/update_favorites/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `expert_id=${iconExpertId}`,
    })
    .then(response => {
        hideSpinner(); // Hide the spinner
        if (response.ok) {
            console.log(`running favorites.js ... favorite updated successfully`);
            // Optionally, you could update the UI further here if needed
        } else {
            console.error(`running favorites.js ... failed to update favorite`);
            // Revert the star icon state if the request failed
            if (isFavorite) {
                icon.classList.remove('bi-star');
                icon.classList.add('bi-star-fill');
            } else {
                icon.classList.remove('bi-star-fill');
                icon.classList.add('bi-star');
            }
            alert('Failed to update favorite. Please try again.');
        }
    })
    .catch(error => {
        hideSpinner(); // Hide the spinner
        console.error(`running favorites.js ... error updating favorite: ${error}`);
        // Revert the star icon state if there's an error
        if (isFavorite) {
            icon.classList.remove('bi-star');
            icon.classList.add('bi-star-fill');
        } else {
            icon.classList.remove('bi-star-fill');
            icon.classList.add('bi-star');
        }
        alert('An error occurred while updating favorite. Please try again.');
    });
}



document.addEventListener('DOMContentLoaded', function() {
    console.log(`running favorites.js ... DOM content loaded`);
    console.log(`running favorites.js ... current origin is: ${ window.location.origin }`);

    jsFavoriteIconMonitor();

});