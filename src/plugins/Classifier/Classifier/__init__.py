"""
This is where the implementation of the plugin code goes.
The Classifier-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('Classifier')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Classifier(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        META = self.META
        active_node = self.active_node

        places = []
        placesPaths = []
        arcs = []
        transitions = []
        transitionPaths = []

        # Traverse and capture all nodes
        nodes = core.load_children(active_node)
        for node in nodes:
            if core.is_type_of(node, META['Place']):
                places.append(node)
            elif (core.is_type_of(node, META['Transition-Place']) or core.is_type_of(node, META['Place-Transition'])):
                arcs.append(node)
            elif core.is_type_of(node, META['Transition']):
                transitions.append(node)

        # Storing Places and Transitions respectively into arrays
        for place in places:
                placesPaths.append(core.get_path(place))

        for transition in transitions:
            transitionPaths.append(core.get_path(transition))

        def isFreeChoice():
            """
            If the intersection of the inplaces sets of two transitions are not empty,
            then the two transitions should be the same (or in short, each transition
            has its own unique set of inplaces)
            """
            for path in transitionPaths:
                inplaceCounter = 0
            for arc in arcs:
                if path == core.get_pointer_path(arc, 'dst'):
                    inplaceCounter = inplaceCounter + 1
            if inplaceCounter > 1:
                return False
            return True

        def isStateMachine():
            # A petri net is a state machine if every transition has exactly one inplace and one outplace.
            for path in transitionPaths:
                inplaceCounter = 0

                for arc in arcs:
                    if path == core.get_pointer_path(arc, 'dst'):
                        inplaceCounter = inplaceCounter + 1
                if inplaceCounter > 1:
                    return False

            for path in transitionPaths:
                outplaceCounter = 0
                for arc in arcs:
                    if path == core.get_pointer_path(arc, 'src'):
                        outplaceCt = outplaceCounter + 1
                if outplaceCounter > 1:
                    return False
            return True

        def isMarkedGraph():
            # A petri net is a marked graph if every place has exactly one out transition and one in transition.
            for path in placesPaths:
                inplaceCounter = 0
                for arc in arcs:
                    if path == core.get_pointer_path(arc, 'dst'):
                        inplaceCounter = inplaceCounter + 1
                if inplaceCounter != 1:
                    return False

            for path in placesPaths:
                inplaceCounter = 0
                for arc in arcs:
                    if path == core.get_pointer_path(arc, 'src'):
                        inplaceCounter = inplaceCounter + 1
                if inplaceCounter != 1:
                    return False  

            return True

        FreeChoiceNotification = isFreeChoice()
        StateMachineNotification = isStateMachine()
        MarkedGraphNotification = isMarkedGraph()

        self.send_notification(F"Free Choice - {FreeChoiceNotification}")
        self.send_notification(F"StateMachine - {StateMachineNotification}")
        self.send_notification(F"Marked Graph - {MarkedGraphNotification}")
