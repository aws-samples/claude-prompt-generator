# Instruction Guide

## Be clear & direct

Suggest Edits When interacting with Claude, providing clear and direct instructions is essential for achieving the best results. Think of Claude like a smart but new employee who has no context on what to do aside from what you explicitly tell them. Just as when you instruct a human for the first time on a task, the more you explain exactly what you want in a straightforward manner, the better and more accurate Claude's response will be.

### Provide detailed context and instructions

To ensure Claude understands your task, provide as much context and detail as possible. Include any specific rules or requirements for completing the task correctly. Consider the following example where we ask Claude to remove personally identifiable information (PII) from a given text:

```
Please remove all personally identifiable information from this text: {{TEXT}}
```

While this prompt may work for simple cases, it lacks the necessary details for Claude to consistently deliver the desired output. Here is a more detailed and clearly written version.

```
We want to anonymize some text by removing all personally identifiable information (PII).
Please follow these steps:
1. Replace all instances of names, phone numbers, and home and email addresses with 'XXX'.
2. If the text contains no PII, copy it word-for-word without replacing anything.
3. Output only the processed text, without any additional commentary.
Here is the text to process:
{{TEXT}}
```

In this improved prompt, we:
1. Provide context upfront about the nature of the task
2. Define what constitutes PII (names, phone numbers, addresses)
3. Give specific, enumerated step-by-step instructions on how Claude should carry out its task
4. Give guidelines to Claude for how it should format its output

### Use numbered lists or bullet points

When providing instructions for complex tasks, consider breaking them down into numbered steps or bullet points. This format makes it easier for Claude to follow the instructions and ensures that all requirements are met.

Here is an example prompt without this technique:

```
Turn this textbook chapter into a lesson plan: {{CHAPTER}}
```

Here is the same prompt with numbered steps:

```
Your task is turn the given textbook chapter into a comprehensive lesson plan. To do this task, you should:
1. Extract and summarize key concepts by section
2. Convert each extracted concept into a 30 minute lesson plan, including a list of questions to check comprehension.
3. Design an accompanying homework assignment that reinforces learnings from this chapter.
Here is the chapter:
<chapter>
{{CHAPTER}}
</chapter>
```

By presenting the instructions as numbered steps, you will both naturally write with more detail and better ensure that Claude executes its task to your standards.

### Be specific about what you want

If you want Claude to provide a definitive answer or take a specific stance on a topic, make that clear in your prompt. When instructions are vague or open-ended, Claude may provide a more general response.

Here is an example of an open-ended question that causes Claude to equivocate:

```
Who is the best basketball player of all time?
```

Here is the same request, but with a more detailed and nuanced ask that successfully pushes Claude to have an opinion:

```
Who is the best basketball player of all time? Yes, there are differing opinions, but if you absolutely had to pick one player, who would it be?
```

### The golden rule of clear prompting

When crafting your prompts, follow the golden rule of clear prompting: show your prompt to a friend or colleague and ask them to follow the instructions themselves to see if they can produce the exact result you want. If your friend is confused, Claude will likely be confused as well.

Remember, Claude is a powerful tool, but it relies on your guidance to deliver the best results. By providing clear, direct, and well-structured prompts, you can unlock Claude's full potential and achieve your desired outcomes more consistently.

## Use examples

Suggest EditsExamples are one of the most powerful tools for enhancing Claude's performance and guiding it to produce your desired output. By providing a few well-crafted examples in your prompt, you can significantly improve the accuracy, consistency, and quality of Claude's responses. This technique is particularly effective for tasks that are highly detailed or require structured outputs or adherence to specific formats.

```
This technique is also known as few-shot prompting (or one-shot prompting if only one example is provided).
```

### Crafting effective examples

To get the most out of using examples in your prompts, consider the following guidelines on how to provide the most effective examples:

* **Relevance:** Ensure that your examples closely resemble the types of inputs and outputs you expect Claude to handle. The more similar the examples are to your actual use case, the better Claude will perform.
* **Diversity:** Include a variety of examples that cover different scenarios, edge cases, and potential challenges. This helps Claude generalize better and handle a wider range of inputs.
* **Clarity:** Make your examples clear, concise, and easy to understand. Use formatting tags like `<example>` to structure your examples and distinguish them from the rest of the prompt. Give Claude context as to what kind of example it's about to encounter when possible (e.g., `Here are some examples of proper APA citations` or `Here are some examples of emails I've written`).
* **Quantity:** While there's no hard rule for the optimal number of examples, aim to provide at least 3-5 examples to start to give Claude a solid foundation. You can always add more targeted examples if Claude's performance isn't meeting your expectations.

To provide examples, simply include them in your prompt, clearly distinguishing them from the actual task. We recommend using `<example></example>` tags to wrap your examples, making it easy for Claude to differentiate between the examples and the rest of the prompt.

Here's a prompt that demonstrates the use of examples to guide Claude's response:

```
I will give you some quotes. Please extract the author from the quote block.
Here is an example:
<example>
Quote: "When the reasoning mind is forced to confront the impossible again and again, it has no choice but to adapt." ― N.K. Jemisin, The Fifth Season
Author: N.K. Jemisin
</example>
Quote:
"Some humans theorize that intelligent species go extinct before they can expand into outer space. If they're > correct, then the hush of the night sky is the silence of the graveyard."
― Ted Chiang, Exhalation
```

In this prompt, the example provides Claude with guidance on how to extract the author's name from a given quote, making it easy for Claude to replicate the process on a new input.

### Formatting outputs

Examples are particularly effective for tasks that require structured or formatted outputs. Sometimes, instead of providing step-by-step formatting instructions, you can simply include a few examples of the desired output format (although we recommend having both instructions and examples together, as that is likely to be more effective than one without the other).

Suppose you want Claude to extract names and professions from a given text and format them as a list. Here's how you might prompt Claude with examples:

```
<example>
Text: Sarah Martinez, a dedicated nurse, was known for her compassionate care at the local hospital. David Thompson, an innovative software engineer, worked tirelessly on groundbreaking projects.
Output:
1. Sarah Martinez [NURSE]
2. David Thompson [SOFTWARE ENGINEER]
</example>
<example>
Text: Chef Oliver Hamilton has transformed the culinary scene with his farm-to-table restaurant. Just down the street, you'll find the library, where head librarian Elizabeth Chen has worked diligently to create a welcoming space for all.
Output:
1. Oliver Hamilton [CHEF]
2. Elizabeth Chen [LIBRARIAN]
</example>
Text: At the town's bustling farmer's market, you'll find Laura Simmons, a passionate organic farmer known for her delicious produce. In the community center, Kevin Alvarez, a skilled dance instructor, has brought the joy of movement to people of all ages.
```

By observing these examples, Claude learns to extract the relevant information and format it as a numbered list with names and professions in the desired style.

### A word of caution

While examples are incredibly powerful, it's important to be mindful of potential pitfalls. Claude may sometimes pick up on unintended patterns in your examples, leading to overfitting or unexpected behaviors.

For instance, if all your example emails end with "Sincerely," Claude might learn to always sign off that way for emails it generates, even if it's not appropriate for every case. To mitigate this, ensure your examples are diverse and representative of the full range of desired outputs.

### Iterating and refining

Crafting the perfect set of examples often involves iteration and refinement. If Claude's performance isn't quite meeting your expectations, consider the following:

* **Analyze the output:** Look for patterns in Claude's responses that deviate from what you want. This can help you identify areas where your examples might be unclear or misleading, or where more examples might help.
* **Add more examples:** If Claude struggles with certain types of inputs, provide additional examples that specifically address those scenarios.
* **Revise existing examples:** Sometimes, even small tweaks to your examples can make a big difference. Experiment with different wordings, formats, or structures to see what works best.
* **Get Claude's help:** Writing good examples is hard! You can ask Claude to evaluate the diversity or relevance of your examples for a given task, or generate new examples given a set of existing examples to reference.

Remember, prompt engineering is an iterative process. Don't be discouraged if your initial examples don't yield perfect results – with a bit of tweaking and experimentation, you'll be able to unlock Claude's full potential and achieve exceptional results for your applications.

## Give a role

Suggest Edits Claude is a highly capable AI assistant, but sometimes it benefits from having additional context to understand the role it should play in a given conversation. By assigning a role to Claude, you can prime it to respond in a specific way, improve its accuracy and performance, and tailor its tone and demeanor to match the desired context. This technique is also known as role prompting.

### When to use role prompting

While role prompting is not always necessary, it can be incredibly useful in the following scenarios:

* **Highly technical tasks:** If you need Claude to perform complex tasks related to logic, mathematics, or coding, assigning an appropriate role can help it excel at the task, even if it might have struggled without the role prompt. Even if Claude isn't struggling, role prompting might still improve performance to new levels.
* **Specific communication styles:** When you require a particular tone, style, or level of complexity in Claude's responses, role prompting can be an effective way to achieve the desired output.
* **Enhancing baseline performance:** Unless you are severely limited by token count, there is rarely a reason not to use role prompting if you want to try improving Claude's performance beyond its baseline capabilities.

### Role prompting examples

Here are a few examples that demonstrate the power of role prompting:

#### Solving a logic puzzle

Let's consider the following logic puzzle:

`There are two ducks in front of a duck, two ducks behind a duck and a duck in the middle. How many ducks are there?`

By assigning the role of a logic bot, Claude's performance improves significantly and it is able to catch the nuance that multiple answers are possible:

```
You are a master logic bot designed to answer complex logic problems. Solve this logic puzzle. There are two ducks in front of a duck, two ducks behind a duck and a duck in the middle. How many ducks are there? 
```

#### Explaining a concept to different audiences

Role prompting can be used to adjust Claude's communication style based on the intended audience. Consider the following prompts and how Claude's output differs depending on the assigned role:

```
You are a kindergarten teacher. Succinctly explain why the sky is blue to your students.
```

### Tips for effective role prompting

To get the most out of role prompting, keep these tips in mind:

1. **Be specific:** Provide clear and detailed context about the role you want Claude to play. The more information you give, the better Claude can understand and embody the desired role.
2. **Experiment and iterate:** Try different roles and variations of your prompts to find the best approach for your specific use case. Prompt engineering often involves experimentation and iteration to achieve optimal results.

# Use XML tags

Suggest EditsXML tags are a powerful tool for structuring prompts and guiding Claude's responses. Claude is particularly familiar with prompts that have XML tags as Claude was exposed to such prompts during training. By wrapping key parts of your prompt (such as instructions, examples, or input data) in XML tags, you can help Claude better understand the context and generate more accurate outputs. This technique is especially useful when working with complex prompts or variable inputs.

> Looking for more advanced techniques? Check out long context window tips to learn how XML tags can help you make the most of Claude's extended context capabilities.

### Why use XML tags?

There are several reasons why you might want to incorporate XML tags into your prompts:

1. **Improved accuracy:** XML tags help Claude distinguish between different parts of your prompt, such as instructions, examples, and input data. This can lead to more precise parsing of your prompt and thus more relevant and accurate responses, particularly in domains like mathematics or code generation.
2. **Clearer structure:** Just as headings and sections make documents easier for humans to follow, XML tags help Claude understand the hierarchy and relationships within your prompt.
3. **Easier post-processing:** You can also ask Claude to use XML tags in its responses, making it simpler to extract key information programmatically.

### How to use XML tags

You can use XML tags to structure and delineate parts of your prompt from one another, such as separating instructions from content, or examples from instructions.

```
Please analyze this document and write a detailed summmary memo according to the instructions below, following the format given in the example:
<document>
{{DOCUMENT}}
</document>
<instructions>
{{DETAILED\_INSTRUCTIONS}}
</instructions>
<example>
{{EXAMPLE}}
</example>
```

#### Handling variable inputs

When working with prompt templates that include variable inputs, use XML tags to indicate where the variable content should be inserted, such as in the following example:

```
I will tell you the name of an animal. Please respond with the noise that animal makes.
<animal>{{ANIMAL}}</animal>
```

As a general rule, you should ways separate your variable inputs from the rest of your prompt using XML tags. This makes it clear to Claude where the examples or data begin and end, leading to more accurate responses.

#### Requesting structured output

You can ask Claude to use XML tags in its responses to make the output easier to parse and process:

```
Please extract the key details from the following email and return them in XML tags:
- Sender name in <sender></sender> tags
- Main topic in <topic></topic> tags
- Any deadlines or dates mentioned in <deadline></deadline> tags
<email>
From: John Smith
To: Jane Doe
Subject: Project X Update
Hi Jane,
I wanted to give you a quick update on Project X. We've made good progress this week and are on track to meet the initial milestones. However, we may need some additional resources to complete the final phase by the August 15th deadline.
Can we schedule a meeting next week to discuss the budget and timeline in more detail?
Thanks,
John
</email>
```

XML tags make it easier to retrieve targeted details from Claude's response by allowing for programmatic extraction of content between specific tags.

### XML best practices

To get the most out of XML tags, keep these tips in mind:

* Use descriptive tag names that reflect the content they contain (e.g., `<instructions>`, `<example>`, `<input>`).
* Be consistent with your tag names throughout your prompts.
* Always include both the opening (`<tag>`) and closing (`</tag>`) tags, including when you reference them, such as `Using the document in <doc></doc> tags, answer this question.`
* You can and should nest XML tags, although more than five layers of nesting may decrease performance depending on the complexity of the use case.

## Chain prompts

Suggest EditsYou can think of working with large language models like juggling. The more tasks you have Claude handle in a single prompt, the more liable it is to drop something or perform any single task less well. Thus, for complex tasks that require multiple steps or subtasks, we recommend breaking those tasks down into subtasks and chaining prompts to ensure highest quality performance at every step.

### What is prompt chaining?

Prompt chaining involves using the output from one prompt as the input for another prompt. By chaining prompts together, you can guide Claude through a series of smaller, more manageable tasks to ultimately achieve a complex goal.

Prompt chaining offers several advantages:

* Improved accuracy and consistency in the generated output at each distinct step
* Easier troubleshooting by isolating specific subtasks that may be particularly error-prone or challenging to handle

### When to use prompt chaining

Consider using prompt chaining in the following scenarios:

1. **Multi-step tasks:** If your task requires multiple distinct steps, such as researching a topic, outlining an essay, writing the essay, then formatting the essay, chaining prompts can help ensure each step of the task has Claude's full focus and is executed at a high level of performance.
2. **Complex instructions:** When a single prompt contains too many instructions or details, Claude may struggle to follow them consistently. Breaking the task into a series of chained subtasks can improve performance for each subtask.
3. **Verifying outputs:** You can use chaining to ask Claude to double-check its own outputs with a given rubric and improve its response if needed, ensuring higher quality results. For example, after generating a list of items, you can feed that list back to Claude and ask it to verify the list's accuracy or completeness.
4. **Parallel processing:** If your task has multiple independent subtasks, you can create separate prompts for each subtask and run them in parallel to save time.

### Tips for effective prompt chaining

1. **Keep subtasks simple and clear:** Each subtask should have a well-defined objective and simple instructions. This makes it easier for Claude to understand and follow.
2. **Use XML tags:** Enclosing inputs and outputs in XML tags can help structure the data and make it easier to extract and pass on to the next step when chaining prompts.

### Examples

Here are a few examples showcasing how to use chaining prompts and breaking tasks into subtasks:

#### Answering questions using a document and quotes

Here we want Claude to, given a document and a question, generate an answer using relevant quotes from the document.

Prompt 1: Extracting the quotes

```
Here is a document, in <document></document> XML tags:
<document>
{{DOCUMENT}}
</document>
Please extract, word-for-word, any quotes relevant to the question {{QUESTION}}. Please enclose the full list of quotes in <quotes></quotes> XML tags. If there are no quotes in this document that seem relevant to this question, please say "I can't find any relevant quotes".
```

Prompt 2 (using `{{QUOTES}}` output from Prompt 1): Answering the question

```
I want you to use a document and relevant quotes from the document to answer a question.
Here is the document:
<document>
{{DOCUMENT}}
</document>
Here are direct quotes from the document that are most relevant to the question:
<quotes>
{{QUOTES}}
</quotes>
Please use these to construct an answer to the question "{{QUESTION}}"
Ensure that your answer is accurate and doesn't contain any information not directly supported by the quotes.
```

#### Validating outputs

In this example, the goal is to have Claude identify grammatical errors in an article, then double-check that the list of errors is complete.

Prompt 1: Generating a list of errors

```
Here is an article:
<article>
{{ARTICLE}}
</article>
Please identify any grammatical errors in the article. Please only respond with the list of errors, and nothing else. If there are no grammatical errors, say "There are no errors."
```

Prompt 2 (using `{{ERRORS}}` output from Prompt 1): Double checking that the list is comprehensive

```
Here is an article:
<article>
{{ARTICLE}}
</article>
Please identify any grammatical errors in the article that are missing from the following list:
<list>
{{ERRORS}}
</list>
If there are no errors in the article that are missing from the list, say "There are no additional errors."
```

#### Parallel processing

In this example, the goal is to have Claude explain a concept to readers at three different levels (1st grade, 8th grade, college freshman) by first creating an outline, then expanding it into a full explanation.

Prompt 1 (create three different versions, one for each reading level): Create an outline

```
Here is a concept: {{CONCEPT}}
I want you to write a three sentence outline of an essay about this concept that is appropriate for this level of reader: {{LEVEL}}
Please only respond with your outline, one sentence per line, in <outline></outline> XML tags. Don't say anything else. 
```

Prompt 2 (using `{{OUTLINE}}` output from Prompt 1, one per reading level): Create full explanations using the outline

```
Here is an outline:
<outline>
{{OUTLINE}}
</outline>
Please expand each sentence in the outline into a paragraph. Use each sentence word-for-word as the first sentence in its corresponding paragraph. Make sure to write at a level appropriate for this type of reader: {{LEVEL}}.
```

## Let Claude think

Suggest EditsWhen faced with a complex question or task, it's often beneficial to let Claude think through the problem step-by-step before providing a final answer. This technique, also known as chain of thought (CoT) prompting, can significantly improve the accuracy and nuance of Claude's responses.

### How to prompt for thinking step-by-step

The simplest way to encourage thinking step-by-step is to include the phrase "Think step by step" in your prompt. For example:

```
Are both the directors of Jaws and Casino Royale from the same country? Think step by step. |
```

For more complex queries, you can guide Claude's thinking by specifying the steps it should take. Here's an example:

```
Use the following clues to answer the multiple-choice question below, using this procedure:
1. Go through the clues one by one and consider whether each is potentially relevant
2. Combine the relevant clues to reason out the answer to the question
3. Map the answer to one of the multiple choice options: (a), (b), or (c)
Clues:
1. Miss Scarlett was the only person in the lounge.
2. The person with the pipe was in the kitchen.
3. Colonel Mustard was the only person in the observatory.
4. Professor Plum was not in the library nor the billiard room.
5. The person with the candlestick was in the observatory.
Question: Was Colonel Mustard in the observatory with the candlestick?
(a) Yes; Colonel Mustard was in the observatory with the candlestick
(b) No; Colonel Mustard was not in the observatory with the candlestick
(c) Unknown; there is not enough information to determine whether Colonel Mustard was in the observatory with the candlestick 
```

By outlining a clear thinking process, you help Claude focus its reasoning on the most relevant information and ensure it thinks through all the necessary factors to perform well at its given task.

### Capturing Claude's thought process

To make it easier to separate Claude's step-by-step reasoning from its final response, consider using XML tags like `<thinking>` and `<answer>`. You can instruct Claude to place its thought process inside `<thinking>` tags and its ultimate answer within `<answer>` tags.

Here's an example prompt with this method:

```
[Rest of prompt] Before answering the question, please think about it step-by-step within <thinking></thinking> tags. Then, provide your final answer within <answer></answer> tags. 
```

### Some considerations

While encouraging step-by-step thinking can greatly enhance Claude's responses, keep these points in mind:

* Thinking cannot occur unless Claude is allowed to output its thought process. There's no way to have Claude think privately and only return the final answer.
* Prompting for step-by-step reasoning will increase the length of Claude's outputs, which can impact latency. Consider this tradeoff when deciding whether to use this technique.

## Control output format (JSON mode)

Suggest EditsClaude is highly capable of producing output in a wide variety of formats. By providing clear instructions, examples, and prefilled responses, you can guide Claude to generate responses that adhere to your desired structure and style.

### Specifying the desired format

One of the simplest ways to control Claude's output is to simply state the format you want. Claude can understand and follow instructions related to formatting, and format outputs such as:

* JSON
* XML
* HTML
* Markdown
* CSV
* Custom formats

For example, if you want Claude to generate a haiku in JSON format, you can use a prompt like this:

```
Please write a haiku about a cat. Use JSON format with the keys "first\_line", "second\_line", and "third\_line".
```

### Providing examples

In addition to explicit instructions, providing examples of the desired output format can help Claude better understand your requirements. When including examples, make it clear that Claude should follow the formatting of the examples provided (otherwise Claude may pick up other details from the provided examples, such as content or writing style).

Here is an example prompt showcasing this technique:

```
Your task is to write a poem. Here are some examples of ideal formatting for the poem:
<poem>
Title: "Autumn Leaves"
Verse 1:
Crisp autumn leaves dance
In the gentle, chilly breeze
A colorful sight
Verse 2:
Red, orange, and gold
Painting the world with beauty
Before winter comes
</poem>
<poem>
Title: "Moonlit Night"
Verse 1:
Moonlight casts shadows
Across the tranquil garden
A peaceful retreat
Verse 2:
Stars twinkle above
As crickets sing their nightsong
Nature's lullaby
</poem>
Now, please write a poem about a sunset, following the formatting of the examples above.
```

---

### Tips for better output control

* Be as specific as possible in your instructions
* Use clear and consistent formatting in your prompts
* Provide multiple examples when possible to reinforce the desired format
* Experiment with different combinations of techniques to find what works best for your use case

## Long context window tips

Suggest EditsClaude's extended context window (200K tokens for Claude 3 models) enables it to handle complex tasks that require processing large amounts of information. Claude's extended context window also enables you to simplify workflows that previously required splitting inputs to fit within shorter context windows. By combining inputs into a single prompt, you can streamline your process and take full advantage of Claude's capabilities.

For example, if your previous application required splitting a long document into multiple parts and processing each part separately, you can now provide the entire document to Claude in a single prompt. This not only simplifies your code but also allows Claude to have a more comprehensive understanding of the context, potentially leading to better results.

> Looking for general prompt engineering techniques? Check out our prompt engineering guide.

### Structuring long documents

When working with long documents (particularly 30K+ tokens), it's essential to structure your prompts in a way that clearly separates the input data from the instructions. We recommend using XML tags to encapsulate each document. This structure is how Claude was trained to take long documents, and is thus the structure that Claude is most familiar with:

XML
```
Here are some documents for you to reference for your task:

<documents>
<document index="1">
<source>
(a unique identifying source for this item - could be a URL, file name, hash, etc)
</source>
<document_content>
(the text content of the document - could be a passage, web page, article, etc)
</document_content>
</document>
<document index="2">
<source>
(a unique identifying source for this item - could be a URL, file name, hash, etc)
</source>
<document_content>
(the text  content of the document - could be a passage, web page, article, etc)
</document_content>
</document>
...
</documents>

[Rest of prompt]

```

This structure makes it clear to Claude which parts of the prompt are input data and which are instructions, improving its ability to process the information accurately. You can also add tags to house other metadata, such as `<title>` or `<author>`.


### Document-query placement

Notice in the above example of long document prompt structure that the documents come first and the rest of the prompt comes after. For situations with long documents or a lot of additional background content, Claude generally performs noticeably better if the documents and additive material are placed up top, above the detailed instructions or user query.

This is true of all Claude models, from legacy models to the Claude 3 family.


### Tips for document q&a

When using Claude for document question-answering tasks, keep these tips in mind:

* Place the question at the end of the prompt, after the input data. As mentioned, this has been shown to significantly improve the quality of Claude's responses.
* Ask Claude to find quotes relevant to the question before answering, and to only answer if it finds relevant quotes. This encourages Claude to ground its responses in the provided context and reduces hallucination risk.
* Instruct Claude to read the document carefully, as it will be asked questions later. This primes Claude to pay close attention to the input data with an eye for the task it will be asked to execute.

Here's an example prompt that incorporates these tips:

```
I'm going to give you a document. Read the document carefully, because I'm going to ask you a question about it. Here is the document: <document>{{TEXT}}</document>
First, find the quotes from the document that are most relevant to answering the question, and then print them in numbered order in <quotes></quotes> tags. Quotes should be relatively short. If there are no relevant quotes, write "No relevant quotes" instead.
Then, answer the question in <answer></answer> tags. Do not include or reference quoted content verbatim in the answer. Don't say "According to Quote [1]" when answering. Instead make references to quotes relevant to each section of the answer solely by adding their bracketed numbers at the end of relevant sentences.
Thus, the format of your overall response should look like what's shown between the <examples></examples> tags. Make sure to follow the formatting and spacing exactly.
<examples>
[Examples of question + answer pairs, with answers written exactly like how Claude's output should be structured]
</examples>
If the question cannot be answered by the document, say so.
Here is the first question: {{QUESTION}}
```

### Multiple choice question generation

When using Claude to generate multiple choice questions based on a given text, providing example question-answer pairs from other parts of the same text can significantly improve the quality of the generated questions. It's important to note that generic multiple choice examples based on external knowledge or generated from an unrelated document do not seem to be nearly as effective.

Here's an example prompt for multiple choice question generation:

```
Your task is to generate multiple choice questions based on content from the following document:
<document>
{{DOCUMENT}}
</document>
Here are some example multiple choice questions and answers based on other parts of the text:
<examples>
Q1: [Example question 1, created from information within the document]
A. [Answer option A]
B. [Answer option B]
C. [Answer option C]
D. [Answer option D]
Answer: [Correct answer letter]
Q2: [Example question 2, created from information within the document]
A. [Answer option A]
B. [Answer option B]
C. [Answer option C]
D. [Answer option D]
Answer: [Correct answer letter]
</examples>
Instructions:
1. Generate 5 multiple choice questions based on the provided text.
2. Each question should have 4 answer options (A, B, C, D).
3. Indicate the correct answer for each question.
4. Make sure the questions are relevant to the text and the answer options are all plausible.
```

By providing example questions and answers from the same text, you give Claude a better understanding of the desired output format and the types of questions that can be generated from the given content.

> For more information on this specific task, see Anthropic's blog post Prompt engineering for a long context window.