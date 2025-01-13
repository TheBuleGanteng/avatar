import { csrfToken, jsScrollDown, updateProfileForm } from './utils.js';



// The JS below retrieves the logged-in user's message history to display in the sidebar
document.addEventListener('DOMContentLoaded', function() {
    console.log(`running retrieveChatHistory.js ... DOM content loaded`);
    
    
    function jsPopulateChatHistorySidebar() {
        console.log(`running jsPopulateChatHistorySidebar ... function started`);

        const chatHistoryParentDiv = document.getElementById('chat-history-div')

        if (chatHistoryParentDiv) {
            
            // Send the form data using fetch API
            fetch('/aichat/retrieve-chat-history/', {
                method: 'GET',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}, error: ${ response.error }`);
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    console.log(`running jsPopulateChatHistorySidebar() ... data is: ${ data }`);
                    
                    // Create a Set to store unique stream IDs
                    const uniqueStreamIds = new Set();

                    data.message_data.forEach(message => {
                        // Check if the stream ID is unique
                        if (!uniqueStreamIds.has(message.session_id)) {
                            uniqueStreamIds.add(message.session_id);
                            
                            const chatHistoryConvo = document.createElement("button");
                            chatHistoryConvo.setAttribute('class', 'row m-1 p-1 border border-secondary d-inline-block');
                            chatHistoryConvo.setAttribute('id', `chatHistoryConvo-${data.stream_id}`);
                            chatHistoryConvo.setAttribute('name', `chatHistoryConvoItem`);
                            chatHistoryConvo.textContent = `${message.session_id}`;

                            const fieldName = 'conversation_id';
                            const fieldValue = message.session_id;

                            chatHistoryConvo.addEventListener('click', () => {
                                jsLoadChatConversation(data, message.session_id);
                                updateProfileForm(fieldName, fieldValue);

                            });
                            chatHistoryParentDiv.append(chatHistoryConvo)
                        }
                    })
                } else {
                    console.error('Response data does not contain message_data property');
                }
            })
        }
    }
    jsPopulateChatHistorySidebar();



    //---------------------------------------------------------------------------------


    function jsLoadChatConversation(data, session_id) {
        console.log(`running jsLoadChatConversation ... function started with data: ${ data } and session_id: ${ session_id }`);

        const feedDiv = document.getElementById('feedDiv')

        if (feedDiv) {
            feedDiv.innerHTML = ''; // Clear the feed of any existing content

            const conversationStreamIds = new Set(); // Declare set to hold only the exchanges in the given convo

            data.message_data.forEach(message => {

                // Check if the stream ID is unique
                if (session_id == message.session_id) {
                    conversationStreamIds.add(message.session_id);
                    
                    if (message.message.startsWith("User:")) {
                        // Create the parent feed item for question
                        const questionFeedItemOuterDiv = document.createElement("div");
                        questionFeedItemOuterDiv.setAttribute(`class`, 'row w-100 justify-content-end d-flex flex-column align-items-end');
                        questionFeedItemOuterDiv.setAttribute(`id`, `questionFeedItemOuterDiv-${ message.session_id }`);
                        questionFeedItemOuterDiv.setAttribute(`name`, `feedItem`);
                        feedDiv.appendChild(questionFeedItemOuterDiv);

                        // Create the child feed item for the question
                        const questionFeedItemInnerDiv2 = document.createElement("div");
                        questionFeedItemInnerDiv2.setAttribute('class', 'border border-secondary border-1 rounded mt-1 mb-1 p-1 d-inline-block w-auto text-bg-dark');
                        questionFeedItemInnerDiv2.setAttribute('id', `questionFeedItemInnerDiv2-${ message.session_id }`);
                        questionFeedItemInnerDiv2.textContent = message.message;
                        questionFeedItemOuterDiv.appendChild(questionFeedItemInnerDiv2);
                    } else {
                        // Create the parent feed item for the answer
                        const answerFeedItemOuterDiv = document.createElement("div");
                        answerFeedItemOuterDiv.setAttribute('class', 'col-lg-10');
                        answerFeedItemOuterDiv.setAttribute(`id`, `answerFeedItemOuterDiv-${ message.session_id }`);
                        answerFeedItemOuterDiv.setAttribute(`name`, `feedItem`);
                        document.getElementById('feedDiv').appendChild(answerFeedItemOuterDiv);

                        // Create the child feed item for the answer
                        const answerFeedItemInnerDiv = document.createElement("div");
                        answerFeedItemInnerDiv.setAttribute('class', 'border border-dark border-2 rounded mt-5 mb-3 p-1 d-inline-block w-auto');
                        answerFeedItemInnerDiv.setAttribute(`id`, `answerFeedItemInnerDiv-${ message.session_id }`);
                        answerFeedItemInnerDiv.textContent = message.message;
                        answerFeedItemOuterDiv.appendChild(answerFeedItemInnerDiv);  
                    } 
                }
            })
            jsScrollDown(); 
        }
    }
});