from powerml import Generator
from powerml import CreateTopicsModel
import nltk
from nltk.stem import WordNetLemmatizer

from math import ceil

unblocked_human_unprompted_1gram_topics = [
    "SourceMarks",
    "VSCode",
    "Web",
    "Dashboard",
    "Kotlin",
    "Styles",
    "Services",
    "Video",
    "Messages",
    "Threads",
    "Mentions",
    "Git",
    "GitHub",
    "Auth",
    "Hub",
    "Slack",
    "Webhooks",
    "Gradle",
    "Intercom",
    "Adminconsole",
    "Ingestion",
    "Api",
    "Onboarding",
    "Discussions",
    "Insights",
    "Email",
    "Teams",
    "Notifications",
    "Pusher",
    "Logging",
    "Security",
    "Commands",
    "Controllers",
    "Stores",
    "Datastores",
    "Test",
    "Typescript",
    "React",
    "Recommendations",
    "Logs",
    "Compression",
    "Compute",
    "Webpack",
    "Webextension"]


class TopicGenerator(Generator):
    '''
    This is a class that can be used to generate more messages for CreateTopicsModels.
    '''

    def __init__(self, gold_topics=unblocked_human_unprompted_1gram_topics):
        nltk.download('wordnet')
        self.lemmatizer = WordNetLemmatizer()
        super().__init__([self.lemmatizer.lemmatize(topic.lower())
                          for topic in gold_topics])

    def coverage_generator(self, messages, return_metrics=True):
        model = CreateTopicsModel()
        model.fit(messages, 'one-word system components')
        generated_topics = [self.lemmatizer.lemmatize(
            topic.lower()) for topic in model.predict()]
        metrics = self.compute_coverage(generated_topics)
        coverage = metrics['Coverage']
        rare_topics = metrics['Rare Types']
        generated_messages = []
        if rare_topics:
            # generate at least 1 example per rare_topic, proportional to the amount of coverage of the messages
            num_generate = ceil(
                (1 - coverage) * len(messages) / len(rare_topics))
            print(f'num generate: {num_generate}')
            for topic in rare_topics:
                modifier = f'include the topic \'{topic}\''
                generated_messages.extend(self._generate_modified(
                    messages, modifier, num_generate))
        if return_metrics:
            return generated_messages, metrics
        return generated_messages
