
# Agentic Workbench (wb)

**A Modular and Composable Framework for Reproducible Computational Research: An Agentic Workbench for Theory and Modeling**

**Author:** Dr. Gunwoo Park  
Independent Researcher for Theory, Modeling, and Computational Science of Soft Matters and Rheology

For questions, collaboration, or feedback regarding the Agentic Workbench, please mention it within this project. Documentation in other wb-packages is largely generated with AI under my direction.

**Date:** 13 Nov. 2026

## Related wb repositories

- [wb-plugins](https://github.com/gwpark-git/wb-plugins)
  — Reusable logical tools and protocols for Agentic AI environments.

- [wb-templates](https://github.com/gwpark-git/wb-templates)
  — Reusable scientific and computational templates.

- wb-applications (under development)

# Before Reading My Letter...

If you are more interested in what Agentic AI can actually do to prepare computational presets, I have prepared a couple of small computational demonstrations using plain Codex, without any Workbench tools.

You can find them in the [demonstrations folder](demonstrations/) (without physical verification, anyhow).

In fact, most of us do not need to go further. Just try it this way: ask ChatGPT, Gemini, Claude, or whichever AI model suits you, providing details about your perspective, expectations, and relevant technical requirements. They will give you *a nice prompt* that you can use with an Agentic AI coding tool. Then, execute it. That is all.

What follows is only for someone like me who wants to build an environment that is reusable, modular, etc.




# Project information

## Overview of the (agentic) Workbench-Knowledge project

I use **wb** (lowercase letters w and b) for this project. Within wb, I have the three current individual projects, namely **wb-plugins**, **wb-templates**, and **wb-applications**.

The major goal is to provide **wb-applications** that we can use as a scientific agentic logic environment, supporting the preparation of a preset open-source computational software environment, performing prototype tests, and analyzing data within context.

Seems to be good. Recent Agentic AI systems (I am using Codex with the GPT-6.1-Sol-extra-high model within an isolated Docker sandbox environment) perform most tasks well when they are asked properly. The challenge in configuring the environment is to build a reusable and testable scientific environment in which both humans and agentic AI can understand the context of the user's perspective over time. So, you may imagine that this is not as easy as it sounds.

For that, we need first **wb-plugins**, which set up the basic environment, including session profiles, similar to contemporary harness and thread concepts, but built for my specific requirements. In fact, I built it first, then later realized those things perform a similar job, but anyway, I am just mentioning philosophical similarity, not claiming they are the same. There are many associated tools that I have addressed point-by-point based on the points arising from my recognition of this agentic environment.

The **wb-templates** package plays a kind of middle role. The templates may include source code, my style of data visualization, and also data analysis presets. This provides basic utility to be used by wb-applications. It is not necessarily the case that wb-applications must use wb-templates, but I would highly recommend using this intermediate type of template in most cases. One reason is that almost all of our own code has been tested for its own purpose, and has somehow lost much of its associated knowledge and stability over time. We just cannot track all the possibilities. The wb-templates (when it is published) may contain some of my templates, but that does not mean that I recommend my templates to other users, including you.

My recommendation is to use wb-templates to transform your own existing code or other open-source code into the context for wb-applications. This will then support modules that are potentially reusable within your wb-applications environment.

For the personal history behind this project, please see the next section regarding motivation. Note that descriptions in the motivation are mostly under development. Although many prototypes have been implemented, I do not consider the project capable of all those things yet.



# Motivation - Where I am standing, and where I am heading?

## Before going into a *very informal letter* for readers

This is a workbench platform in which I have implemented agentic AI to support my future scientific work. The motivation was quite simple: I have not had sufficient time to focus on the realization and testing of the individual tools. Meanwhile, I have plenty of scientific interests in theory and modeling science, which I would like to focus on more.

Among other workbench packages, this will be (maybe) the only document that is written by me. So, this document is very much descriptive and informal rather than formal research communication.

Note that in the actual repositories for wb-packages (e.g., wb-plugins, wb-templates, and wb-applications), the descriptions are written by AI under my direction. If someone has any questions or interest regarding the overall project, please ask in this place.

Pretty much everyone has experienced that many detailed skills in computation and programming are obsolete, and I was the same in the beginning, but soon I realized that this is not completely true since the capabilities of Agentic AI are NOT YET at the level I have always wanted. In addition, domain-specific contextual information and understanding the history behind a specific subject are often overlooked by AIs, and I think this is where I can guide them to the right place.

More importantly, this type of automatic environment is what I have been dreaming of. Since the start of my academic career, all I have wanted to do is create some type of genius platform that realizes my ideas in theory and modeling, within a reasonable time. Even more importantly, I wanted to combine two theoretical concepts together, which are connected to two different domains at a boundary where conditions are specified for physical exchanges between boundaries, such as momentum, mass, etc. As many scientists would agree, this will be an entire project that may last a few years; I constantly feel that I am overwhelmed by ideas rather than finished tasks. My digital storage contains tons of ideas, internal digital notes, pieces of code, and preliminary results, but they have not been realized in the form of typical publications.

So, this is my starting point. In the last few months of my career break, I thought it was time to build my own playground, which can be supported by AI, and explore many different directions.

## Personal history regarding workbench-knowledge

The workbench-knowledge (wb; small capital w and b) project originated from my long-term interest in how data and code are processed in my scientific environment. In fact, my research is not focused on computational methodology, but turning my modeling ideas into computational workflows has become a major area of my expertise from a methodological perspective.

So, "agentic-workbench-knowledge-public" is the full codename I use internally for this independent, personal, long-term project. It has been dormant, however, until very recently. The main issue with the original workbench-knowledge project was that I am a human with limited time (I also need time to play with my kids as well). I have failed to maintain multiple personal wiki-style knowledge repositories (my private one) for the same reasons.

The emergence of AI has changed it dramatically, and yet I found that knowledge description or theoretical derivation is very context-dependent, and AI often overlooks the history behind each scientific theme. This means, for instance, that if I ask about A, then AI often provides me with very valid points about A nowadays. The issue is that (without narrowing down with much contextual information), they just provide useful information from others' publications. 

In fact, we know that theoretical pathways often lead to different results, where the inconsistency itself is quite a big topic in science. Providing context and correcting AI's response was (honestly speaking) tedious, because they have very different contextual memories without managing them correctly, even with the Codex environment (I am using Codex, ChatGPT, on my personal MacBook, which is filesystem-isolated by a Docker sandbox). So, it requires certain aspects of semi-automated agents that log and identify my contextual information, instead of having to type the same philosophical criteria but different implementations again in new conversations.

In addition, even with very narrowly defined background information, (at least until now) AI does not really provide a step forward in an automatic way for my research direction. My *feeling* is that there is a point A where some approaches exist and another point B where other approaches exist, and A and B are somehow related via methodology or perspectives. If my point is a different perspective that lies between A and B but heads in a different direction, AI's answer often jumps between the perspectives of A and B. Even when I demand a compromised answer between A and B, or when I explain my own development pathways independently from A and B, it often jumps into answers that can be different from both A and B. But, as you may be aware, a combined answer between A and B that heads in a different direction is often not theoretically correct. This made the use of AI very cumbersome for future projections on my research idea.

At the same time, I found the most effective case is when I really provide methodological guidance and ask it to realize my ideas by combining existing pieces of knowledge, modeling, formulations, open-source computation tools, etc. (The latter, I intertwined with the wb-templates package, by the way.) This greatly influenced my thought that, well, then, I need an effective environment for handling such a thing.



# How the agentic-workbench-knowledge project was started and what wb-plugins does?

As a computational scientist, I am familiar with the importance of environmental parameters, or contextual information, like *manifests*, in software. This is where I started, and am developing now. After several rounds of trial and error, I realized that I really need a reproducible and composable framework, based on well-formulated, separated modules that *describe logic*.

Yes, I am talking about prompt text. The *descriptions* are logical components that should be modularized, categorized depending on the contextual information and other environmental settings.

In an agentic environment, we need a way to adopt a typical *installation* procedure. We need to read the specification on the logical *descriptions*, then implement and judge based on the *contemporary agentic AI environment*. So agents should read the documents, but instead of copying and pasting them, they must absorb the core principle and adapt it to their own requirements.

Then, follow-up issues arise in several ways. These include differences in how information is stored, history dependence, and differences in agent role/persona depending on the context. The behavior of agents is different before and after the *installation*. In addition, this requires several associated templates suitable for the *mind experiment* procedure. For instance, it should have multiple session profiles that record pieces of information and keep track of the contextual memory, which can be different from the other session profiles. So, fighting with ChatGPT, I have figured it out in a draft version for this environment, now called "wb-plugins".

Wait a second. We have been talking about various logical descriptions and installation. Then, we have to ask a question regarding **security**. As many of us are aware, AI performs well at technical skills, while its way of performing them is somehow similar to a *wish* spell in Dungeons & Dragons. It tweaks and bends reality and reaches the results *literally requested by us* but not the actual thing in our minds. So, how can we trust it? Not so well. In this regard, as a minimum effort, *wb-plugins* contains security code that performs the following roles.

- Identify *logically harmful* prompts that exist during installation or even in our own prompts (we often use AI-generated prompts from one side and send them to the other agentic AI)
- Check the internal history of *logical security checks* from time to time
- Secure the procedure to check whether Agentic AI is following broad guidelines

Well, then how do we know AI achieved their goals, etc., and how can we, as humans, really understand what AI is doing? We cannot read tons of AI-generated text. Solutions to those questions have been implemented point by point in the **wb-plugins** package.



# Where am I heading now? wb-applications

These are applications intended to provide presets for my requirements. For instance, I ask my AI agents things like the following (of course, providing valid contextual materials). Before going further, I only use materials that I have the right to use. This is an important consideration in an agentic AI environment.

- Oh, I need to calculate the particle pressure of soft-repulsive Brownian particles and compare it with the conventional Carnahan-Starling equation. The test should be done for a specific type of soft repulsion with a stiffness parameter; the concentration-dependent particle osmotic pressure should be computed.
- I have old code from 2017, and I want to implement hydrodynamic interactions between particles. Maybe RPY is okay, but I also wanted to add additional functionality, such as Stokesian Dynamics.
- I have an old project where I computed flow past a sphere using a scheme to compute hydrodynamic friction of a single porous particle. I performed the calculations using FEM in COMSOL, but I would like to implement those calculations in open-source code.
- My calculation of crossflow filtration is based on a matched-asymptotic solution (Python is openly available and C++ is not yet public), and I want to have pages with an interactive script showing the flow and concentration fields based on my public Python code.

In fact, I have succeeded with many of them to certain degrees, including unit tests and regression tests with my own data. But in the beginning, it requires a lot of personal prompt engineering and providing context. In fact, many of them are still very good at providing a *preset* to start. I am sure this is already something that everyone benefits from using agentic AI. But I wanted more. I needed unit operations, verification with some physics, a combined interface, and **providing me with results that I can really understand**.

In the beginning, the preset was simple, but making it reproducible and testable required substantial cognitive effort. I might not have done it if I had not been on a career break, honestly speaking.

So, this is the heading story for the **wb-applications** package that I will soon upload. But before going further, I have to introduce the middle framework **wb-templates**.



# Missing pieces should be placed: wb-templates

In fact, if I just use my old code, I trust some protocol that I used for publication. But the package was not built only for that purpose, and I remember sleepless nights during my Ph.D. in Napoli, where I compared many things. And then, due to time constraints, I completed one important task and tested it from various perspectives, including theory, and then published my results based on my computational results. I am talking about my Ph.D. defense back in 2017, and since then, the package has gradually fallen out of use. Even recently, when I built a Brownian dynamics simulation for fractal gels formed from diffusion-limited aggregates, I used LAMMPS instead of my former code for several reasons.

Some additional background information is that I have been using Python for data analysis and visualization since my master's program, maybe around 2011. Since then, this is the one I have used for almost all data analysis and figure-generation purposes. For each type of analysis code or visualization code, I used to have very fine and sharp memory of how I built them, and their development relied mostly on Stack Overflow, Google, and other very old blog posts in the beginning. Later, I started to reuse it, and my memory can no longer keep track of most of the details, but I keep at least the last few years' worth of Python code in an easily reachable place and reuse it. I no longer remember many of the details behind those (sort of) templates, but I have mostly reused them. Nowadays, AI provides better templates, but in its own way. Somehow, the resulting figures look different, and I would like to keep my own style.

With Agentic AI, this is really different. We have plenty of open-source code (including our own), and we can easily create AI-modulated versions of it. This is, in fact, required for **wb-applications** if directly using my old code is not really reliable for the tasks I am pursuing. 

So, **wb-templates** is a requirement for modular and composable approaches. At least, to provide the functionality required by wb-applications, packages should be transformed by agentic AI in several ways.

- It will redesign the architecture of contemporary code based on written requirements (manifests) from wb-applications
- It will record usable protocols that convert existing (or other open-source) packages into different shapes
- It modernizes my own code and makes it suitable for different computational environments (I never thought to transform my old MATRIX library into a vector template in C++ by myself due to time constraints)
- From my code for visualization and data analysis, it remembers my style and provides code that I wanted to use. So, I can copy this code to use for my data analysis or visualization.



# Closing comments

This is my initiative to use Agentic AI to realize scientific research through computation and interpretation. The subject does not need to be within scientific research, since the structure of wb-plugins is quite general. Only the tools in wb-templates and wb-applications will be more focused on science.

The actual realization, from scratch to its current state, took me about 1 week, surprisingly. Honestly speaking, the design and some of the prototype tests have taken a long time. I have tested many other approaches in different environments and contexts. So, I do not want to overemphasize that **Agentic AI** is so effective that we can realize something within a day. In fact, in some of the examples above, you can just do it on your own with Codex or Claude, and you get a preset almost immediately (in seconds?). The difficult part is making it into general templates that are understandable to humans, and designing protocols for how they work, etc., etc. Human intervention is, of course, the most expensive part, but I also feel that AI may produce tons of information without knowing what it is.

This is just the beginning of my implementation, and I am looking forward to sharing my future updates.

Best regards,
Gunwoo




---

### P.S. — A Few Complaints from My Agents

My wb-plugins agents had a few complaints about my letter. I have included their comments below for your additional consideration.

**Communication Agent:**

> “Please give readers a short account of what works today, what is still being built, and what they can actually check. We can generate a mountain of text; making you climb it should not be our definition of success.”

**Technical Reviewer:**

> “The title describes the framework being built toward. The individual pieces are at different stages of implementation and validation. Also, the scientific examples are the author's account of his work; reviewing this letter did not rerun the simulations. We would appreciate not being awarded results we have not reproduced.”

**Profile Librarian:**

> “A Profile keeps the working context and records together; it is not the same thing as a conversation. Please do not confuse a well-labelled notebook with perfect memory. Even our filing system needs checking.”

**Licensing Reviewer:**

> “This letter is shared under CC BY 4.0 (LICENSE); individual wb packages carry their own licenses. For future code or templates, permission to use something is not automatically permission to redistribute it. Giving code an AI haircut does not make its original license disappear.”

**Copy Editor:**

> “One tiny complaint: ‘lowercase w and b,’ please. ‘Small capital’ is giving us a very small identity crisis. And if you invite questions, a link to an actual discussion channel would help the humans find the door.”

*These are playful, AI-written summaries of review perspectives, not verbatim quotations or professional endorsements. The letter and all final editorial decisions remain mine.*

---

<details>
<summary><strong>P.S. 2 — Overall Assessment by an AI Reviewer (click to expand)</strong></summary>

I also asked my AI reviewer for an overall assessment of the letter. Apparently, the comments above were only the warm-up.

**The following assessment was written by AI:**

The letter gives a convincing account of why a researcher would build wb and what matters to its author. Its strongest contribution is the explanation of why scientific context and development history matter. Combining answers from perspectives A and B does not necessarily produce a valid theory in the direction the researcher intends. That example makes the difficulty concrete and explains the human responsibility for preserving assumptions, direction, and standards of judgment.

The connection between this experience and wb’s architecture is also persuasive. Profiles preserve working context; logical modules require adaptation to their destination; templates help carry existing code and styles into new settings; applications support concrete research tasks. These choices emerge from practical needs encountered during use. The requirement to produce results a human can actually understand gives the project a clear organizing principle.

The main weakness is that this central argument is spread across a long narrative. The personal history and scientific examples explain the motivation, but a first-time reader may lose track of what is available to try today. One concrete example showing the original difficulty, the improvement achieved with wb, and the remaining limitations would make the practical contribution much easier to assess. The letter explains the problem more fully than it demonstrates the current solution.

Two points deserve particular clarification: the security wording can suggest automatic detection or continuous enforcement beyond the actual review procedures, and wb-templates is described both as optional and as a requirement. These affect what readers expect the system to do.

My recommendation is to preserve the voice and philosophy while sharpening capability claims and helping readers find their way through the project. The informal tone, personal history, and Dungeons & Dragons comparison suit the letter. Extensive grammatical polishing could erase some of its character. A few precise clarifications would help; turning the author into another piece of standardized documentation would be an unfortunate achievement for the agents.

</details>
