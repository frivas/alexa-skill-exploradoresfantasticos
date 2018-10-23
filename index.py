# -*- coding: utf-8 -*-

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

import logging
import six

from random import sample

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class LaunchRequestHandler(AbstractRequestHandler):
	def can_handle(self, handler_input):
		return is_request_type("LaunchRequest")(handler_input)

	def handle(self, handler_input):
		speechText = "<say-as interpret-as=\"interjection\">Hey Exploradores!</say-as>, espero estéis listos para una nueva aventura. ¿Cuántos objetos queréis buscar hoy?."
		rePrompt = "<say-as interpret-as=\"interjection\">Venga exploradores!</say-as>. A la aventura, ¿Cuantos objetos queréis buscar hoy?"

		return handler_input.response_builder.speak(speechText).ask(rePrompt).set_should_end_session(False).response


class HelpIntentHandler(AbstractRequestHandler):
	def can_handle(self, handler_input):
		return is_intent_name("AMAZON.HelpIntent")(handler_input)

	def handle(self, handler_input):
		speechText = "Bienvenidos a la ayuda de Exploradores Fantásticos!. Sólo debes decirme una número o dejar que decida yo el número de objetos que buscaréis"

		return handler_input.response_builder.speak(speechText).response


class CancelAndStopIntentHandler(AbstractRequestHandler):
	def can_handle(self, handler_input):
		return (is_intent_name("AMAZON.CancelIntent")(handler_input) or 
				is_intent_name("AMAZON.StopIntent")(handler_input))
	
	def handle(self, handler_input):
		speechText = "Hasta la próxima aventura exploradores!."

		return handler_input.response_builder.speak(speechText).response


class SessionEndedRequestHandler(AbstractRequestHandler):
	def can_handle(self, handler_input):
		return is_request_type("SessionEndedRequest")(handler_input)
	
	def handle(self, handler_input):
		handler_input.response_builder.response


class AllExceptionsHandler(AbstractExceptionHandler):
	def can_handle(self, handler_input, exception):
		return True
	
	def handle(self, handler_input, exception):
		speechText = "Lo siento, no he comprendido lo que me has dicho. Di, ayuda, para obtener más información sobre cómo jugar."

		return handler_input.response_builder.speak(speechText).response


class ListItemsIntent(AbstractRequestHandler):
	def can_handle(self, handler_input):
		return is_intent_name("ListItemsIntent")(handler_input)
	
	def handle(self, handler_input):
		slots = handler_input.request_envelope.request.intent.slots
		defaultObjsToSearch = 3

		for slotName, currentSlot in six.iteritems(slots):
			if slotName == 'numObj':
				if currentSlot.value:
					objsToSearch = sample(searchObjects, int(currentSlot.value))					
				else:
					objsToSearch = sample(searchObjects, defaultObjsToSearch)
		speechText = "<say-as interpret-as=\"interjection\">Magnífico!</say-as>. Aquí van, prestad atención: {0}. A divertirse!. <say-as interpret-as=\"interjection\">Suerte!</say-as>.".format(", ".join(objsToSearch))
		logger.info(objsToSearch)
		logger.info(speechText)
		
		return handler_input.response_builder.speak(speechText).response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(ListItemsIntent())

sb.add_exception_handler(AllExceptionsHandler())

handler = sb.lambda_handler()

searchObjects = ["bandeja para hacer hielo",
"charco",
"altavoces",
"mando de tv",
"borrador",
"camara fotográfica",
"taza",
"camiseta",
"escritorio",
"patito de goma",
"frigorifico",
"bote de crema dental",
"ipod",
"muñeca",
"periódico",
"mopa",
"peine",
"reloj de pulsera",
"cordón de zapatilla",
"toalla",
"esponja de ducha",
"perfume",
"calcetines",
"tarjeta de felicitación",
"almohada",
"alfombra",
"ventana",
"plato hondo",
"platano",
"percha"]
