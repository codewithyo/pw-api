# What is this project?

1. This is a web scrapping process using web APIs available on the website. It require the `Authorization Bearer` KEY to work. So you need to buy these courses in order to use APIs.
2. While this has a Private API. So I am doing a method called `Reverse Engineering of API` to achieve my wants.

# Why this project?

1. I want to get all the resources like _quizzes, assignment_ at one place for everyone.
2. Due to this project my concepts get broader and deeper in the domain of `API`, `GET` and `POST` method in `HTTP` (Web-Dev Domain), `request` module in Python, etc.

# Requirements

You need to have the `Authorization Key` in order to see **your** analytics.

## How to get Authorization Key

#### Steps

1. Open the browser and navigate to the [PW Skills Course Website](https://learn.pwskills.com).
2. Open the developer tools by pressing `F12` or by right-clicking on the page and selecting "Inspect Element".
3. Click on the "Network" tab in the developer tools.
4. Select the request that contains the **Authorization** header. Example Url:
   - https://api.pwskills.com/v1/auth/profile
   - https://api.pwskills.com/v1/learn/section/currentLiveClass/course/63a2eb428899436daf7eb489
5. In the request details, scroll down to the **"Headers"** section and look for the **"Authorization"** header.
6. The value of the Authorization header should start with the word **"Bearer"** followed by a space and then the token itself. Copy the entire header value, including the word **"Bearer"** and the token.

> `Note:` If you are not enrolled in any course you did not get any **Authorization Key**. So you have to pass `'N/A'` as argument in `--auth-key` parameter. [How to pass](#how-to-use)

# How to get Course Id

You can get the **Course Id** from the course url by following the steps:

1. Get the Course URL in my URL of Data Science Course.  
   https://learn.pwskills.com/lesson/Bokeh/640428d0182c67573e4c337a/course/Data-Science-masters/63a2eb428899436daf7eb489
2. In this URL, the course id is followed by the course name.  
   Course Id = `63a2eb428899436daf7eb489`

> `Note:` If you are not enrolled in any course you did not get any **Course Id**. So you have to pass pass the following ID to work on respective courses. [How to pass](#how-to-use)

```json
{
  "Java with DSA and System Design": "63a2f02d889943137f7ec85f",
  "Data Science Masters": "63a2eb428899436daf7eb489",
  "Full Stack Web Development": "63a2ecdd88994300d47eb9ad",
  "Decode DSA with C++": "63eb1ae1194b22195fe5d967"
}
```

# How to Use

1. Get the Authorization Key. [Hint](#how-to-get-authorization-key)
2. Get your Course Id. [Hint](#how-to-get-course-id)
3. Run `main.py` to follow the repo requirements. Use following command:

```sh
python3 main.py --auth-key '<<TOKEN>>' --course-id '<<id>>'
```

4. Finally run the following command to launch the Streamlit Web-App.

```sh
streamlit run app.py
```

# Acknowledgment

This project is the analysis of the courses available on [PW Skills](https://learn.pwskills.com/) website. I bought the Data Science Course. Thats why I am able to get the `Authorization Bearer Token` in order to get data with GET method.

# Data accessing using Authorization Key

1. User Profile Data as `profile.json`

```sh
https://api.pwskills.com/v1/auth/profile
```

2. User Submission Data as `submission.json`

```sh
https://api.pwskills.com/v1/learn/submission/63a2eb428899436daf7eb489
```

3. User Progress Data as `user_progress.json`

```sh
https://api.pwskills.com/v1/learn/analytics/progress/course/63a2eb428899436daf7eb489
```

# Project Progress

- [x] Get all the important APIs and URLs from the PW Skills website using _Network Tab in the browser's Dev-Tool_.
- [x] Learn how to use the **Network Tab** in the browser's Dev-Tool.
- [x] Learn what is `Authorization` header in **Request Header**.
- [x] Make a function to download all the resources like **Quiz, Assignments** using `requests` library.
- [x] Also, make a function to exclude the URLs which are already downloaded.
- [x] A function to download ~~sectionResource practice questions and solutions~~ Google drive shared file using its URL.
- [x] Make proper directory structure.
- [x] Provide a pre-planned data for the end-user to use because what if they have not any `auth-key`?
- [x] UI for Quizzes.
- [ ] UI for personalized analytics for users.
- [x] Page for Assignments and its solutions. Note, the solution links are mine.
- [x] Make a **Streamlit Web-App** to summarize selected course.
- [ ] ~~Make Web-Pages for all the analysis notebook using `BeautifulSoup`.~~ **Not Possible**
- [x] Removed all credentials from directory.

# Release Note

- [ ] **11 March, 2023**. Completed UI development.
