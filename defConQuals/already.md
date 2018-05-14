# You Already Know

After looking the in the html, css, and json files, I noticed that "if you can read this" was emphasized.

During the iFixit Triatholon (an event White Hat and iFixit put on every year), [@atila](https://github.com/atti1a) wrote a few web challenges in which flags were hidden in the headers and such.

I opened the developers tools to get a look at what was happening on the webpage, and I saw several requests that looked normal. Then, I click on the challenge, and I noticed that three requests were sent out when the challenge was clicked: a fetch, script, and a font request.

Then, I determined that the fetch was probably of interest. On inspection of the response message, I noticed that there was a comment inside of the message.

```Stop overthinking it, you already know the answer here. [comment]: <> (OOO{Sometimes, the answer is just staring you in the face. We have all been there}) You already have the flag. **Seriously**, _if you can read this_, then you have the flag. Submit it! 
```
The comment contained the flag: OOO{Sometimes, the answer is just staring you in the face. We have all been there}
