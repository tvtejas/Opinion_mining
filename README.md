# Opinion_mining
Due to the development of e-commerce and web technology, most of online Merchant sites
enable writing comments about purchasing products for customer. Customer reviews
expressed opinion about products or services which are collectively referred to as customer
feedback data. Opinion extraction about products from customer reviews is becoming an
interesting area of research and it is motivated to develop an automatic opinion mining
application for users. Therefore, efficient method and techniques are needed to extract
opinions from reviews.

For a popular product, the number of reviews can be in hundreds or even in thousands,
which is difficult to be read one by one. Therefore, automatic extraction and summarization
of opinion are required for each feature. When a user expresses opinion for a product,
he/she states about the product as a whole or about its features one by one. Feature
identification in product is the first step of opinion mining application and opinion words
extraction is the second step which is critical to generate a useful summary by classifying
polarity of opinion for each feature. Therefore, we must extract opinion for each feature of a
product.

In this, given a set of customer reviews of a particular product, we need to perform the
following tasks: (1) identifying product feature that customer commented on; (2) extracting
opinion words or phrases through adjective, adverb, verb, and noun and (3) determining the
orientation of the opinion words.
We use a part-of-speech tagger to identify phrases in the input text that contains adjective or
adverb or verb or nouns as opinion phrases. A phrase has a positive semantic orientation
when it has good associations (e.g., “awesome camera”) and a negative semantic
orientation when it has bad associations (e.g., “low battery”).
