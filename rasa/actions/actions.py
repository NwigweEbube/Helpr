# rasa/actions/actions.py

import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionRunWorkflow(Action):
    def name(self) -> Text:
        return "action_run_workflow"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Example: Trigger a Node-RED workflow via an HTTP request
        try:
            response = requests.post("http://node_red:1880/trigger_workflow",
                                     json={"user_id": tracker.sender_id})
            if response.ok:
                dispatcher.utter_message(text="Workflow started successfully!")
            else:
                dispatcher.utter_message(text="Failed to start workflow. Please try again later.")
        except Exception as e:
            dispatcher.utter_message(text=f"Error connecting to automation service: {str(e)}")
        return []
