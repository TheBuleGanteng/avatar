from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
import logging



logger = logging.getLogger('django')



def stream_response_to_user(
    conversation_id,
    user_input,
    user,
):
    def event_stream():
        
        # Initialize message history. Note that we pass in chat history window.
        user_id = user.id
        user_profile = user.aichat_userprofile

        chat_history_window_int = user_profile.chat_history_window
        
        preferred_language = user_profile.preferred_language
        retriever_model = user_profile.retriever_model
        model_provider = retriever_models_supported.get(retriever_model, {}).get('model_provider', 'Unknown')
        temperature = user_profile.temperature
        top_p = user_profile.top_p
        logger.info(f'running stream_response_to_user ... '
                    f'user is: { user }'
                    f'retriever_model is: { retriever_model },  '
                    f'model_provider is: { model_provider }'
                    f'temperature is: { temperature }, and '
                    f'top_p is: { top_p }')

        if model_provider == 'Anthropic':
            # Instructions for Anthropic API: https://python.langchain.com/docs/integrations/chat/anthropic/, https://python.langchain.com/api_reference/anthropic/chat_models/langchain_anthropic.chat_models.ChatAnthropic.html
            model = ChatAnthropic(
                model=retriever_model,
                temperature=user_profile.temperature,
                max_tokens=1024,
                timeout=None,
                max_retries=2,
                top_p=top_p,
                # other params...
            )
        else:
            # Instructions for OpenAI API
            model = ChatOpenAI(
                model=retriever_model, # EXPOSE LATER
                streaming=True,  # Enable streaming
                temperature=temperature,
                top_p=top_p,
            )
        logger.debug(f"running stream_response_to_user() ... model is: { model }")

        # Detect user input language and use this for translation of key phrases
        try:
            detected_language = preferred_language
            #detected_language = detect_language(user_input)
        except Exception as e:
            logger.error(f'running stream_response_to_user() ... unable to determine detected language, falling back to "en"')
            detected_language = 'en'
        logger.debug(f'running stream_response_to_user() ... '
                     f'user_input is: { user_input } and '
                     f'detected_language is: { detected_language }')

        if detected_language == None:
            detected_language = user_profile.preferred_language
            logger.error(f'running stream_response_to_user() ... detected_language was None, '
                         f'falling back to user.aichat_userprofile.preferred_language: { detected_language }')


        # Step 2: Translate key phrases, if needed
        if detected_language != "en":
            context_available_phrase_translated = translate(
                input_text=context_available_phrase,
                from_language="en",
                to_language=detected_language,
            )
            chat_history_phrase_translated = translate(
                input_text=chat_history_phrase,
                from_language="en",
                to_language=detected_language,
            )
            no_answer_phrase_translated = translate(
                input_text=no_answer_phrase,
                from_language="en",
                to_language=detected_language,
            )
            general_knowledge_phrase_translated = translate(
                input_text=general_knowledge_phrase,
                from_language="en",
                to_language=detected_language,
            )
            sources_translated = translate(input_text="Sources:", from_language="en", to_language=detected_language)
            page_translated = translate(input_text="page", from_language="en", to_language=detected_language)
        else:
            context_available_phrase_translated = context_available_phrase
            chat_history_phrase_translated = chat_history_phrase
            no_answer_phrase_translated = no_answer_phrase
            general_knowledge_phrase_translated = general_knowledge_phrase
            sources_translated = "Sources:"
            page_translated = "page"
            
        logger.debug(
            f"running stream_response_to_user() ... context_available_phrase_translated is: { context_available_phrase_translated }, "
            f"running stream_response_to_user() ... chat_history_phrase_translated is: { chat_history_phrase_translated }, "
            f"running stream_response_to_user() ... no_answer_phrase_translated is: { no_answer_phrase_translated }, "
            f"running stream_response_to_user() ... general_knowledge_phrase_translated is: { general_knowledge_phrase_translated }, and "
            f"running stream_response_to_user() ... sources_translated is: { sources_translated }"
        )

        # Step 1: Send begin of stream message
        yield "id: {}\ndata: [BEGIN]\n\n".format(1)

        # Step 3: Select the appropriate system prompt relative to use general knowledge bool      
        data_source = user_profile.data_source
        logger.debug(f"running stream_response_to_user() ... for user: { user }, data_source is: { data_source }")
        if data_source == 'hist_rag_web':
            use_general_knowledge_bool = True
        else:
            use_general_knowledge_bool = False
        logger.debug(f'running stream_response_to_user ... '
                     f'use_general_knowledge_bool type is: {type(use_general_knowledge_bool)}, '
                     f'use_general_knowledge_bool value is: {use_general_knowledge_bool}')
        
        
        # Step 3: Use LangChain's ChatPromptTemplate to combine the system instructions, conversation history, and user input into a single prompt
        if data_source == 'rag':
            ignore_chat_history_bool = True
        else:
            ignore_chat_history_bool = False
        logger.debug(f'running stream_response_to_user ... '
                    f'ignore_chat_history_bool is: { ignore_chat_history_bool }')
        
        # Select the correct system prompt according to whether the user has toggled on web access
        system_prompt = generate_system_prompt(ignore_chat_history_bool=ignore_chat_history_bool, use_general_knowledge_bool=use_general_knowledge_bool)
        logger.info(f'running stream_response_to_user() ... '
                    f'use_general_knowledge_bool is: { use_general_knowledge_bool }, '
                    f'ignore_chat_history_bool is: { ignore_chat_history_bool }, and '
                    f'system_prompt is: { system_prompt }')

        if ignore_chat_history_bool:
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    # MessagesPlaceholder(variable_name="history"), Ignores chat history
                    ("human", "{input}"),
                ]
            )
        else:
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    MessagesPlaceholder(variable_name="history"),
                    ("human", "{input}"),
                ]
            )

        # Step 4: Set up LangChain's runnable framework which is used to manage how prompts and user inputs are sent to the OpenAI model while maintaining context.
        runnable = prompt | model

        # Step 5: Invoke LangChain's RunnableWithMessageHistory, we pass both the retrieved document, and the conversation history.
        with_message_history = RunnableWithMessageHistory(
            runnable,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
            history_factory_config=[
                ConfigurableFieldSpec(
                    id="user_id",
                    annotation=str,
                    name="User ID",
                    description="Unique identifier for the user.",
                    default="",
                    is_shared=True,
                ),
                ConfigurableFieldSpec(
                    id="conversation_id",
                    annotation=str,
                    name="Conversation ID",
                    description="Unique identifier for the conversation.",
                    default="",
                    is_shared=True,
                ),
                ConfigurableFieldSpec(  # Add chat_history_window_int to match the function signature
                    id="chat_history_window_int",
                    annotation=int,
                    name="Chat History Window",
                    description="Number of prior messages to include in chat history.",
                    default=None,
                    is_shared=True,
                ),
            ],
        )
        logger.debug(f'running stream_response_to_user() ... with_message_history is: { with_message_history }')


        # Step 6: Retrieve the relevant docs
        retriever = set_up_retriever(user)  
        if not retriever:
            logger.error(f'running stream_response_to_user() ... failed create or access the retriever')
            return JsonResponse({'status': 'error', 'message': 'Error: failed create or access the retriever'}, status=500)
        logger.debug(f'running stream_response_to_user() ... sucessfully pulled retriever: { retriever }')

        #retrieved_chunks = retriever.vectorstore.similarity_search_with_score(user_input)
        retrieved_chunks = retriever.invoke(user_input)
        logger.debug(f'running stream_response_to_user() ... '
                     f'user_input is: { user_input } and '
                     f'retrieved_chunks is: { retrieved_chunks }')
        
        # Separate the retrieved sources into documents and websites
        context = []

        
        #similarity_threshold = 0.7
        #for chunk, score in retrieved_chunks:
        for chunk in retrieved_chunks:
            logger.debug(f'running stream_response_to_user() ... chunk is: { chunk }')
            context.append(chunk.page_content.strip())
            #context.append(f"{chunk.page_content.strip()} (Score: {score:.2f})")
        # Join the list entries to form a single string for context
        context = ' '.join(context)
        logger.debug(f'running stream_response_to_user() ... context is: { context }')
            
        # Step 8: Append each answer chunk as it comes in, passing in user_input
        answer_chunks = []  # Initiate a list to hold the chunks of a given response

        event_id = 2
        response_length = user_profile.response_length

        # Here, 'chunk' represents a chunk in the streamed answer
        for chunk in with_message_history.stream(
            {
                "language": detected_language,
                "input": user_input,
                "context": context,
                "chat_history_phrase_translated": chat_history_phrase_translated,
                "context_available_phrase_translated": context_available_phrase_translated,
                "no_answer_phrase_translated": no_answer_phrase_translated,
                "general_knowledge_phrase_translated": general_knowledge_phrase_translated,
                "response_length": response_length,
            },
            config={"configurable": {"user_id": user_id, "conversation_id": conversation_id, "chat_history_window_int": chat_history_window_int,}},
        ):
            logger.debug(f'running stream_response_to_user() ... chunk is: { chunk }')
            
            # Append the chunk to answer_chunks (this consolidated answer is used for topic extraction and expert recommendation)
            answer_chunks.append(chunk.content)
            
            yield "id: {}\ndata: {}\n\n".format(event_id, chunk.content)
            event_id += 1
            time.sleep(0.1)  # Adjust the delay as needed


        answer_text = "".join(answer_chunks)
        
        # If an answer was streamed to the user, proceed with listing sources and experts (if recommendations are turned on)
        if context_available_phrase_translated in answer_text:
            logger.debug(f'running stream_response_to_user() ... neither '
                    f'no_answer_phrase { no_answer_phrase_translated }, nor '
                    f'general_knowledge_phrase_translated: { general_knowledge_phrase_translated } '
                    f'are in answer_text: { answer_text }, '
                    f'proceeding to list sources ')

            contributing_chunks = []
            #used_text_chunks = [chunk.page_content for chunk in used_chunks]
            #for chunk in retrieved_chunks:
            #for chunk, score in retrieved_chunks:
            # Capture the source(s) contributing to this chunk
            #text_chunks = [chunk.page_content for chunk, _ in retrieved_chunks]
            #text_chunks = [chunk.page_content for chunk in retrieved_chunks]]
            
            similarities = calculate_similarities(
                retrieved_chunks = retrieved_chunks, 
                answer_text = answer_text, 
                user=user,
            )

            for chunk, similarity in zip(retrieved_chunks, similarities):
            #for (chunk, _), similarity in zip(retrieved_chunks, similarities):
                                
                if chunk.metadata['type'] == 'document':
                    doc_name = chunk.metadata['source']
                    doc_chunk_link_url = f"{settings.MEDIA_URL}{user.id}/{doc_name}"
                    doc_chunk_link = f'<a href="{doc_chunk_link_url}" target="_blank">{doc_name}</a>'
                    chunk_key = f"{doc_chunk_link}, {page_translated}, {int(chunk.metadata['page_number'])}<br>"

                elif chunk.metadata['type'] == 'website':
                    title = chunk.metadata.get('title', 'No Title Available')  # Fallback if title is missing
                    chunk_url = chunk.metadata.get('source')
                    chunk_url_formatted = f'<a href="{chunk_url}" target="_blank">{chunk_url}</a>'
                    chunk_key = f"{ title }, { chunk_url_formatted }<br>"

                contributing_chunks.append((chunk_key, similarity))
                #contributing_chunks.append((chunk_key, score))
                #contributing_chunks.append(chunk_key)
            logger.debug(f'running stream_response_to_user() ... '
                        f'contributing_chunks is: { contributing_chunks }')
            
            min_source_score = 0.75
            ranked_sources_deduplicated = []
            for source in contributing_chunks:
                if source not in ranked_sources_deduplicated and float(source[1][0]) >= min_source_score: # source[0] is the total score for each source, as returned by the calculate_similarities function
                    ranked_sources_deduplicated.append(source)
            
            ranked_sources = sorted(ranked_sources_deduplicated, key=lambda x: x[1][0], reverse=True)[:1] # EXPOSE LATER
            #ranked_sources = contributing_chunks[:1]
            logger.info(f'running stream_response_to_user() ... '
                        f'ranked_sources is: { ranked_sources }')

            # Stream the traslated version of the phrase 'Sources:'
            yield "id: {}\ndata: <br><br><b>{}</b><br>\n\n".format(event_id, sources_translated)
            
            for source, _ in ranked_sources: # Since deduplicated_sources_sorted is a tuple containing both a source and its associated score, here, we only care about the source. The use of '_' allows us to skip over the second item in the tuple (e.g the score), since that is not needed in printing the sources. 
            #for source in ranked_sources:
                yield "id: {}\ndata: {}\n\n".format(event_id, source)
                event_id += 1
        
        
            # Step 16: Use if statement to extract question topic and recommend experts only if suggest_experts is toggled on
            number_of_experts = int(user_profile.experts_suggested_number)
        
            if user_profile.suggest_experts and number_of_experts > 0:
                    
                related_experts = retrieve_experts(
                        input_text = user_input + answer_text, 
                        number_of_experts = number_of_experts,
                        detected_language = detected_language,
                        user = user,
                    )
            
                logger.debug(f"running stream_response_to_user() ... after running retrieve_experts(), related_experts is: { related_experts }")
                for expert in related_experts:
                    yield f"id: {event_id}\ndata: Expert: {json.dumps(expert)}\n\n"
                    event_id += 1

            else:
                logger.debug(f"running stream_response_to_user() ... no topic extracted")

        # Step 22: Send end of stream message
        yield "id: {}\ndata: [END]\n\n".format(event_id)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")
