document.addEventListener('DOMContentLoaded', function() {
    console.log(`running slider_equalization.js ... DOM content loaded`);
    console.log(`running slider_equalization.js ... current origin is: ${ window.location.origin }`);


    function toPercentage(value) {
        return (value * 100).toFixed(0) + '%';
    }
    
    // Select the recommendation weight sliders
    let recommendationWeightYears = document.getElementById('recommendation-weight-years');
    let recommendationWeightIndustry = document.getElementById('recommendation-weight-industry');
    let recommendationWeightRole = document.getElementById('recommendation-weight-role');
    let recommendationWeightTopic = document.getElementById('recommendation-weight-topic');
    
    // Show the initial values in the value box
    const recommendationWeightYearsValueBox = document.getElementById('recommendation-weight-years-value-box');
    recommendationWeightYearsValueBox.innerHTML = parseFloat(recommendationWeightYears.value);

    const recommendationWeightIndustryValueBox = document.getElementById('recommendation-weight-industry-value-box');
    recommendationWeightIndustryValueBox.innerHTML = parseFloat(recommendationWeightIndustry.value);

    const recommendationWeightRoleValueBox = document.getElementById('recommendation-weight-role-value-box');
    recommendationWeightRoleValueBox.innerHTML = parseFloat(recommendationWeightRole.value);

    const recommendationWeightTopicValueBox = document.getElementById('recommendation-weight-topic-value-box');
    recommendationWeightTopicValueBox.innerHTML = parseFloat(recommendationWeightTopic.value);


    // Define the listener and what happens when a change is detected in years
    recommendationWeightYears.addEventListener('change', function () {
        console.log(`running slider_equalization.js ... change in recommendation weight for years detected`)

        recommendationWeightYearsValue = parseFloat(recommendationWeightYears.value);
        recommendationWeightIndustryValue = parseFloat(recommendationWeightIndustry.value);
        recommendationWeightRoleValue = parseFloat(recommendationWeightRole.value);
        recommendationWeightTopicValue = parseFloat(recommendationWeightTopic.value);
        console.log(`running slider_equalization.js ... new value for recommendationWeightYearsValue is: ${recommendationWeightYearsValue}`)

        // Calculate overflow
        const totalOtherWeights = recommendationWeightIndustryValue + recommendationWeightRoleValue + recommendationWeightTopicValue;
        const recommendationValueOverflow = totalOtherWeights - (1 - recommendationWeightYearsValue);

        // Adjust other weights
        recommendationWeightIndustryValue -= recommendationValueOverflow / 3;
        recommendationWeightRoleValue -= recommendationValueOverflow / 3;
        recommendationWeightTopicValue -= recommendationValueOverflow / 3;

        // Ensure no negative values
        recommendationWeightIndustryValue = Math.max(recommendationWeightIndustryValue, 0);
        recommendationWeightRoleValue = Math.max(recommendationWeightRoleValue, 0);
        recommendationWeightTopicValue = Math.max(recommendationWeightTopicValue, 0);

        // Update the sliders with new values
        recommendationWeightIndustry.value = recommendationWeightIndustryValue.toFixed(2);
        recommendationWeightRole.value = recommendationWeightRoleValue.toFixed(2);
        recommendationWeightTopic.value = recommendationWeightTopicValue.toFixed(2);

        // Update the value boxes with new values
        recommendationWeightYearsValueBox.innerHTML = recommendationWeightYears.value;
        recommendationWeightIndustryValueBox.innerHTML = recommendationWeightIndustry.value;
        recommendationWeightRoleValueBox.innerHTML = recommendationWeightRole.value;
        recommendationWeightTopicValueBox.innerHTML = recommendationWeightTopic.value;

        console.log(`running slider_equalization.js ... New value for recommendationWeightIndustryValue is: ${recommendationWeightIndustryValue}`);
        console.log(`running slider_equalization.js ... New value for recommendationWeightRoleValue is: ${recommendationWeightRoleValue}`);
        console.log(`running slider_equalization.js ... New value for recommendationWeightTopicValue is: ${recommendationWeightTopicValue}`);

    });

    // Define the listener and what happens when a change is detected in industry
    recommendationWeightIndustry.addEventListener('change', function () {
        console.log(`running slider_equalization.js ... change in recommendation weight for industry detected`)

        recommendationWeightYearsValue = parseFloat(recommendationWeightYears.value);
        recommendationWeightIndustryValue = parseFloat(recommendationWeightIndustry.value);
        recommendationWeightRoleValue = parseFloat(recommendationWeightRole.value);
        recommendationWeightTopicValue = parseFloat(recommendationWeightTopic.value);
        console.log(`running slider_equalization.js ... new value for recommendationWeightIndustryValue is: ${recommendationWeightIndustryValue}`)

        // Calculate overflow
        const totalOtherWeights = recommendationWeightYearsValue + recommendationWeightRoleValue + recommendationWeightTopicValue;
        const recommendationValueOverflow = totalOtherWeights - (1 - recommendationWeightIndustryValue);

        // Adjust other weights
        recommendationWeightYearsValue -= recommendationValueOverflow / 3;
        recommendationWeightRoleValue -= recommendationValueOverflow / 3;
        recommendationWeightTopicValue -= recommendationValueOverflow / 3;

        // Ensure no negative values
        recommendationWeightYearsValue = Math.max(recommendationWeightYearsValue, 0);
        recommendationWeightRoleValue = Math.max(recommendationWeightRoleValue, 0);
        recommendationWeightTopicValue = Math.max(recommendationWeightTopicValue, 0);

        // Update the sliders with new values
        recommendationWeightYears.value = recommendationWeightYearsValue.toFixed(2);
        recommendationWeightRole.value = recommendationWeightRoleValue.toFixed(2);
        recommendationWeightTopic.value = recommendationWeightTopicValue.toFixed(2);

        // Update the value boxes with new values
        recommendationWeightYearsValueBox.innerHTML = recommendationWeightYears.value;
        recommendationWeightIndustryValueBox.innerHTML = recommendationWeightIndustry.value;
        recommendationWeightRoleValueBox.innerHTML = recommendationWeightRole.value;
        recommendationWeightTopicValueBox.innerHTML = recommendationWeightTopic.value;

        console.log(`running slider_equalization.js ... New value for recommendationWeightYearsValue is: ${recommendationWeightYearsValue}`);
        console.log(`running slider_equalization.js ... New value for recommendationWeightRoleValue is: ${recommendationWeightRoleValue}`);
        console.log(`running slider_equalization.js ... New value for recommendationWeightTopicValue is: ${recommendationWeightTopicValue}`);

    });

    // Define the listener and what happens when a change is detected in role
    recommendationWeightRole.addEventListener('change', function () {
        console.log(`running slider_equalization.js ... change in recommendation weight for role detected`)

        recommendationWeightYearsValue = parseFloat(recommendationWeightYears.value);
        recommendationWeightIndustryValue = parseFloat(recommendationWeightIndustry.value);
        recommendationWeightRoleValue = parseFloat(recommendationWeightRole.value);
        recommendationWeightTopicValue = parseFloat(recommendationWeightTopic.value);
        console.log(`running slider_equalization.js ... new value for recommendationWeightRoleValue is: ${recommendationWeightRoleValue}`)

        // Calculate overflow
        const totalOtherWeights = recommendationWeightYearsValue + recommendationWeightIndustryValue + recommendationWeightTopicValue;
        const recommendationValueOverflow = totalOtherWeights - (1 - recommendationWeightRoleValue);

        // Adjust other weights
        recommendationWeightYearsValue -= recommendationValueOverflow / 3;
        recommendationWeightIndustryValue -= recommendationValueOverflow / 3;
        recommendationWeightTopicValue -= recommendationValueOverflow / 3;

        // Ensure no negative values
        recommendationWeightYearsValue = Math.max(recommendationWeightYearsValue, 0);
        recommendationWeightIndustryValue = Math.max(recommendationWeightIndustryValue, 0);
        recommendationWeightTopicValue = Math.max(recommendationWeightTopicValue, 0);

        // Update the sliders with new values
        recommendationWeightYears.value = recommendationWeightYearsValue.toFixed(2);
        recommendationWeightIndustry.value = recommendationWeightIndustryValue.toFixed(2);
        recommendationWeightTopic.value = recommendationWeightTopicValue.toFixed(2);

        // Update the value boxes with new values
        recommendationWeightYearsValueBox.innerHTML = recommendationWeightYears.value;
        recommendationWeightIndustryValueBox.innerHTML = recommendationWeightIndustry.value;
        recommendationWeightRoleValueBox.innerHTML = recommendationWeightRole.value;
        recommendationWeightTopicValueBox.innerHTML = recommendationWeightTopic.value;

        console.log(`running slider_equalization.js ... New value for recommendationWeightYearsValue is: ${recommendationWeightYearsValue}`);
        console.log(`running slider_equalization.js ... New value for recommendationWeightIndustryValue is: ${recommendationWeightIndustryValue}`);
        console.log(`running slider_equalization.js ... New value for recommendationWeightTopicValue is: ${recommendationWeightTopicValue}`);
    });

    // Define the listener and what happens when a change is detected in topic
    recommendationWeightTopic.addEventListener('change', function () {
        console.log(`running slider_equalization.js ... change in recommendation weight for topic detected`)

        recommendationWeightYearsValue = parseFloat(recommendationWeightYears.value);
        recommendationWeightIndustryValue = parseFloat(recommendationWeightIndustry.value);
        recommendationWeightRoleValue = parseFloat(recommendationWeightRole.value);
        recommendationWeightTopicValue = parseFloat(recommendationWeightTopic.value);
        console.log(`running slider_equalization.js ... new value for recommendationWeightTopicValue is: ${recommendationWeightTopicValue}`)

        // Calculate overflow
        const totalOtherWeights = recommendationWeightYearsValue + recommendationWeightIndustryValue + recommendationWeightRoleValue;
        const recommendationValueOverflow = totalOtherWeights - (1 - recommendationWeightTopicValue);

        // Adjust other weights
        recommendationWeightYearsValue -= recommendationValueOverflow / 3;
        recommendationWeightIndustryValue -= recommendationValueOverflow / 3;
        recommendationWeightRoleValue -= recommendationValueOverflow / 3;

        // Ensure no negative values
        recommendationWeightYearsValue = Math.max(recommendationWeightYearsValue, 0);
        recommendationWeightIndustryValue = Math.max(recommendationWeightIndustryValue, 0);
        recommendationWeightRoleValue = Math.max(recommendationWeightRoleValue, 0);

        // Update the sliders with new values
        recommendationWeightYears.value = recommendationWeightYearsValue.toFixed(2);
        recommendationWeightIndustry.value = recommendationWeightIndustryValue.toFixed(2);
        recommendationWeightRole.value = recommendationWeightRoleValue.toFixed(2);

        // Update the value boxes with new values
        recommendationWeightYearsValueBox.innerHTML = recommendationWeightYears.value;
        recommendationWeightIndustryValueBox.innerHTML = recommendationWeightIndustry.value;
        recommendationWeightRoleValueBox.innerHTML = recommendationWeightRole.value;
        recommendationWeightTopicValueBox.innerHTML = recommendationWeightTopic.value;

        console.log(`running slider_equalization.js ... New value for recommendationWeightYearsValue is: ${recommendationWeightYearsValue}`);
        console.log(`running slider_equalization.js ... New value for recommendationWeightIndustryValue is: ${recommendationWeightIndustryValue}`);
        console.log(`running slider_equalization.js ... New value for recommendationWeightRoleValue is: ${recommendationWeightRoleValue}`);

    });
});