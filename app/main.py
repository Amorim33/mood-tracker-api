from datetime import datetime

import speech_recognition as sr
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app.__version__ import __version__

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReadMainResponse(BaseModel):
    message: str = Field(description="Service status message.")
    version: str = Field(description="Service version.")


@app.get("/", response_model=ReadMainResponse)
def service_metadata():
    """
    Get service metadata.
    """
    return ReadMainResponse(
        message="Mood Tracker API is running! 🚀",
        version=__version__,
    )


def sentiment_scores(sentence):
    """
    The sentiment analysis function.
    This function will receive a sentence and return the sentiment score.
    the sentiment score is a float number between -1 and 1,
    where -1 is the saddest sentiment and 1 is the happiest.
    """
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)

    return sentiment_dict["compound"]


class MoodResponse(BaseModel):
    mood: str = Field(description="Mood of the day.")
    date: str = Field(description="Date of the mood.")


@app.post(
    "/api/v1/mood", response_model=MoodResponse, status_code=status.HTTP_202_ACCEPTED
)
def track_mood(file: UploadFile = File(...)):
    """
    The mood tracker endpoint. This endpoint will receive an audio file
    containing the user's day description and return the mood of the day.
    """
    if file.content_type != "audio/wav":
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Audio file must be in WAV format.",
        )

    recognizer = sr.Recognizer()
    with sr.AudioFile(file.file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        score = sentiment_scores(text)
        date = datetime.now().strftime("%Y-%m-%d")

        if score >= 0.05:
            return MoodResponse(mood="Happy", date=date)
        elif score <= -0.05:
            return MoodResponse(mood="Sad", date=date)
        else:
            return MoodResponse(mood="Neutral", date=date)

    except sr.UnknownValueError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google Speech Recognition could not understand audio.",
        )
    except sr.RequestError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not request results from Google Speech Recognition service.",
        )
