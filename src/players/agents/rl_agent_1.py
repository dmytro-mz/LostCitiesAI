import numpy as np
import torch
from numpy.random.mtrand import Sequence
from torch import nn

from src.action import Action
from src.game import GameState
from src.players.agents.base_rl_agent import BaseRLAgent, COLOR_COUNT, CARD_VALUES_COUNT

COMMON_DTYPE = np.float32


class _MyModel1(torch.nn.Module):
    CARD_EMBEDDING_SIZE = 3
    INPUT_SIZE = 234

    def __init__(self, hidden_layers: Sequence[int] = (128, 128)):
        super().__init__()
        self._card_emb_layer = self._linear_relu(COLOR_COUNT + CARD_VALUES_COUNT, self.CARD_EMBEDDING_SIZE)
        self.hidden_layers = [self._linear_relu(self.INPUT_SIZE, hidden_layers[0])] + [
            self._linear_relu(prev_size, next_size)
            for prev_size, next_size in zip(hidden_layers[:-1], hidden_layers[1:])
        ]
        self.output_layer = nn.Linear(hidden_layers[-1], BaseRLAgent.ACTION_SPACE_SIZE)

    @staticmethod
    def _linear_relu(input_size: int, output_size: int) -> nn.modules.module:
        return nn.Sequential(nn.Linear(input_size, output_size), nn.ReLU())

    def forward(self, inputs: tuple) -> torch.Tensor:
        (
            sorted_hand_ohe,
            norm_hand_val_diff_to_own_pile,
            can_opponent_play_my_card,
            top_cards_in_own_pile_ohe,
            norm_own_pile_scores,
            norm_total_own_score,
            top_cards_in_opp_pile_ohe,
            norm_opp_pile_scores,
            norm_total_opp_score,
            top_cards_in_discard_pile_ohe,
            norm_discard_pile_val_diff_to_own_pile,
            draw_deck_size,
        ) = inputs
        sorted_hand_emb = torch.cat([self._card_emb_layer(card) for card in sorted_hand_ohe])
        top_cards_in_own_pile_emb = torch.cat([self._card_emb_layer(card) for card in top_cards_in_own_pile_ohe])
        top_cards_in_opp_pile_emb = torch.cat([self._card_emb_layer(card) for card in top_cards_in_opp_pile_ohe])
        top_cards_in_discard_pile_emb = torch.cat(
            [self._card_emb_layer(card) for card in top_cards_in_discard_pile_ohe]
        )
        model_input = torch.cat(
            (
                sorted_hand_emb,
                norm_hand_val_diff_to_own_pile,
                can_opponent_play_my_card,
                top_cards_in_own_pile_emb,
                norm_own_pile_scores,
                norm_total_own_score,
                top_cards_in_opp_pile_emb,
                norm_opp_pile_scores,
                norm_total_opp_score,
                top_cards_in_discard_pile_emb,
                norm_discard_pile_val_diff_to_own_pile,
                draw_deck_size,
            )
        )
        x = model_input
        for layer in self.hidden_layers:
            x = layer(x)
        return self.output_layer(x)


class RLAgent1(BaseRLAgent):
    def __init__(self, train_buffer, hidden_layers=(128, 128)):
        super().__init__(train_buffer, _MyModel1(hidden_layers))

    def choose_action(self, game_state: GameState) -> Action:
        self._create_local_state()
        model_input = self._create_model_input(game_state)
        action_values = self.model.predict(model_input)
        # TODO select subsequence of valid actions self._get_action_mask(game_state)
        action_idx = self.e_greedy.choose(action_values)
        action = self._get_action_by_index(action_idx)
        self._drop_local_state()
        self._game_train_records.append([model_input, action_idx, None, None])
        return action

    def end_turn(self, game_state_after_action: GameState):
        self._game_train_records[-1][2] = self._create_model_input(game_state_after_action)

    def end_game(self, game_state: GameState):
        final_game_value = game_state.players_piles.get_piles_value()
        for r in self._game_train_records:
            r[-1] = final_game_value
        self.train_buffer.extend(self._game_train_records)

    def _create_model_input(self, game_state: GameState):
        (
            sorted_hand,
            norm_hand_val_diff_to_own_pile,
            can_opponent_play_my_card,
            top_cards_in_own_pile,
            norm_own_pile_scores,
            norm_total_own_score,
            top_cards_in_opp_pile,
            norm_opp_pile_scores,
            norm_total_opp_score,
            top_cards_in_discard_pile,
            norm_discard_pile_val_diff_to_own_pile,
            draw_deck_size,
        ) = self._create_observation(game_state)
        sorted_hand_ohe = [self._card_ohe_encoder(card) for card in sorted_hand]
        top_cards_in_own_pile_ohe = [self._card_ohe_encoder(card) for card in top_cards_in_own_pile]
        top_cards_in_opp_pile_ohe = [self._card_ohe_encoder(card) for card in top_cards_in_opp_pile]
        top_cards_in_discard_pile_ohe = [self._card_ohe_encoder(card) for card in top_cards_in_discard_pile]
        return (
            sorted_hand_ohe,
            norm_hand_val_diff_to_own_pile,
            can_opponent_play_my_card,
            top_cards_in_own_pile_ohe,
            norm_own_pile_scores,
            norm_total_own_score,
            top_cards_in_opp_pile_ohe,
            norm_opp_pile_scores,
            norm_total_opp_score,
            top_cards_in_discard_pile_ohe,
            norm_discard_pile_val_diff_to_own_pile,
            draw_deck_size,
        )
