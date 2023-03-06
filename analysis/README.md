# PW Experience Portal Scrapper ✅

> **Observation:** After hitting these APIs, website get the option to choose the projects from the selection field.

1. API for Techs section : https://internship-api.pwskills.com/project/techs
2. API for Domain section : https://internship-api.pwskills.com/project/domains
3. API for Projects section : https://internship-api.pwskills.com/project/

This contains all the information related to any project like G-Docs links, Titles, etc. Everything which I need to scrape. This project is not called as a Web Scrapping Project instead this called as a Fetching Data From API to make a Dashboard.

### This project is present in another repository [here](https://github.com/arv-anshul/pw-experience-portal).

# More APIs from PW Skills for analysis.

## API for Courses data ✅

1. Get full course details: https://api.pwskills.com/v1/course/63a2eb428899436daf7eb489?withAllCourseMetas=true&ignoreInActive=true
2. Get all the uploaded session details of the live course:
   - https://learn.pwskills.com/_next/data/Ags5MBEe764gpjeSLm3-n/lesson/Multithreading/63eb8cbf194b2213a3e5f4ee/course/Data-Science-masters/63a2eb428899436daf7eb489.json
   - https://learn.pwskills.com/_next/data/Ags5MBEe764gpjeSLm3-n/course/Data-Science-masters/63a2eb428899436daf7eb489.json

## Breakdown of URL ✅

> https://learn.pwskills.com/_next/data/Ags5MBEe764gpjeSLm3-n/lesson/Multithreading/63eb8cbf194b2213a3e5f4ee/course/Data-Science-masters/63a2eb428899436daf7eb489.json

- `https://learn.pwskills.com/` is the website link.
- `Ags5MBEe764gpjeSLm3-n` do not know for now.
- `/lesson/Multithreading/63eb8cbf194b2213a3e5f4ee/` maybe the title and id of the topic/lesson.
- `https://learn.pwskills.com/_next/data/Ags5MBEe764gpjeSLm3-n/course/Data-Science-masters/63a2eb428899436daf7eb489.json` is json file which contains the running course details.

# In order to use these APIs you have to provide the `Authorization` details in the `Request Headers` which are unique for every users.

## PW Course Quiz URLs ❗❗

1. `/quiz/-Files-quiz/63e7b4f1194b220eaee5abe5/course/Data-Science-masters/63a2eb428899436daf7eb489` this is the **pratyay** (suffix) of the quiz url.
2. `https://learn.pwskills.com/quiz/-Files-quiz/63e7b4f1194b220eaee5abe5/course/Data-Science-masters/63a2eb428899436daf7eb489` Full Quiz Url of above mentioned.
3. `https://api.pwskills.com/v1/learn/lesson/course/63a2eb428899436daf7eb489/63e7b4f1194b220eaee5abe5` This is the API request URL of the same quiz.

- Just identify the relation between above 3 urls and then apply the algorithm on it and make a quiz web page out of it.
- Also, check the algorithm behind the solution of the quiz after submission.
- MF it gives error unauthorized. Try to find the solution of it from _request header section in Firefox's Dev Tool's Network Tab_.

## PW Course Quiz Submission API ❗❗

- `https://api.pwskills.com/v1/learn/submission/63a2eb428899436daf7eb489/quiz/63f0e698ff4766b511dc661b` It has also a **request header** (give below as JSON format) because it is a `POST` request.

```json
// This is request payload for submission of a quiz

{
  "answers": [
    { "answer": [true, false, false, false] },
    { "answer": [false, true, false, false] },
    { "answer": [false, true, false, false] },
    { "answer": [true, false, false, false] },
    { "answer": [true, false, false, false] },
    { "answer": [false, false, false, true] },
    { "answer": [true, false, false, false] },
    { "answer": [false, true, false, false] },
    { "answer": [false, false, true, false] },
    { "answer": [false, true, false, false] }
  ],
  "g-recaptcha-response": "<<BIG-STRING>>"
}
```

# User Submission Data

- [`submission.json`](../data/others/submission.json) is json response contains the quiz and assignment submission data.
- cURL command to get submission.json response.

```sh
curl 'https://api.pwskills.com/v1/learn/submission/63a2eb428899436daf7eb489'
 -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
 -H 'Accept: application/json, text/plain, */*'
 -H 'Accept-Language: en-US,en;q=0.5'
 -H 'Accept-Encoding: gzip, deflate, br'
 -H 'Referer: https://learn.pwskills.com/'
 -H 'Authorization: Bearer <<TOKEN>>'
 -H 'Origin: https://learn.pwskills.com'
 -H 'DNT: 1'
 -H 'Connection: keep-alive'
 -H 'Sec-Fetch-Dest: empty'
 -H 'Sec-Fetch-Mode: cors'
 -H 'Sec-Fetch-Site: same-site'
 -H 'TE: trailers'
```

```sh
curl 'https://api.pwskills.com/v1/learn/lesson/course/63a2eb428899436daf7eb489/63f771b6a9d3a2026eb45887'
 -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
 -H 'Accept: application/json, text/plain, */*'
 -H 'Accept-Language: en-US,en;q=0.5'
 -H 'Accept-Encoding: gzip, deflate, br'
 -H 'Referer: https://learn.pwskills.com/'
 -H 'Authorization: Bearer <<TOKEN>>'
 -H 'Origin: https://learn.pwskills.com'
 -H 'DNT: 1'
 -H 'Connection: keep-alive'
 -H 'Sec-Fetch-Dest: empty'
 -H 'Sec-Fetch-Mode: cors'
 -H 'Sec-Fetch-Site: same-site'
 -H 'TE: trailers'
```

- In this cURL command (OR maybe in all) only `Authorization` header is important nothing else.

```sh
curl 'https://api.pwskills.com/v1/learn/lesson/course/63a2eb428899436daf7eb489/63f771b6a9d3a2026eb45887'
 -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
 -H 'Authorization: Bearer <<TOKEN>>'
```

# Course Analytics

- Users Progress details [user_progress.json](../data/others/user_progress.json)

```sh
curl 'https://api.pwskills.com/v1/learn/analytics/progress/course/63a2eb428899436daf7eb489'
 -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
 -H 'Authorization: Bearer <<TOKEN>>'
```

# Get assignment data

```sh
curl 'https://api.pwskills.com/v1/learn/lesson/course/63a2eb428899436daf7eb489/63fb7e48182c67a2a64b9b0a'
 -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
 -H 'Authorization: Bearer <<TOKEN>>'
```

# Decode the Authorization Bearer token

```json
// Authorization Bearer <<TOKEN>>

{
  "_id": "63a1f5879d90b2b9e65c4012",
  "email": "<email@id>",
  "firstName": "<firstName>",
  "lastName": "<lastName>",
  "iss": "ineuron.ai",    // Issuer (who created and signed this token)
  "iat": 1677595587,    // Issued at (seconds since Unix epoch)
  "exp": 1677681987    // Expiration time (seconds since Unix epoch)
}
```

# For more URL information go to [README.json](README.json)
