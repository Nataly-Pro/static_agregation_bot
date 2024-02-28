from datetime import datetime

from aiogram.types import User, Chat, Message, Update

TEST_USER = User(id=123, is_bot=False, first_name='Test', last_name='Bot', username='testbot',
                 language_code='ru', is_premium=None, added_to_attachment_menu=None, can_join_groups=None,
                 can_read_all_group_messages=None, supports_inline_queries=None)

TEST_USER_CHAT = Chat(id=1234567890, type='private', title=None, username=TEST_USER.username, first_name=TEST_USER.first_name,
            last_name=TEST_USER.last_name, is_forum=None, photo=None, active_usernames=None, available_reactions=None,
            accent_color_id=None, background_custom_emoji_id=None, profile_accent_color_id=None,
            profile_background_custom_emoji_id=None, emoji_status_custom_emoji_id=None,
            emoji_status_expiration_date=None, bio=None, has_private_forwards=None,
            has_restricted_voice_and_video_messages=None, join_to_send_messages=None, join_by_request=None,
            description=None, invite_link=None, pinned_message=None, permissions=None, slow_mode_delay=None,
            message_auto_delete_time=None, has_aggressive_anti_spam_enabled=None, has_hidden_members=None,
            has_protected_content=None, has_visible_history=None, sticker_set_name=None, can_set_sticker_set=None,
            linked_chat_id=None, location=None)


def get_message(text: str):
    return Message(message_id=123, date=datetime.now(), chat=TEST_USER_CHAT, message_thread_id=None, from_user=TEST_USER,
                   sender_chat=None, sender_boost_count=None, forward_origin=None, is_topic_message=None,
                   is_automatic_forward=None, reply_to_message=None, external_reply=None, quote=None,
                   reply_to_story=None, via_bot=None, edit_date=None, has_protected_content=None, media_group_id=None,
                   author_signature=None,
                   text=text,
                   entities=None, link_preview_options=None, animation=None, audio=None, document=None, photo=None, sticker=None,
                   story=None, video=None, video_note=None, voice=None, caption=None, caption_entities=None, has_media_spoiler=None,
                   contact=None, dice=None, game=None, poll=None, venue=None, location=None, new_chat_members=None,
                   left_chat_member=None, new_chat_title=None, new_chat_photo=None, delete_chat_photo=None, group_chat_created=None,
                   supergroup_chat_created=None, channel_chat_created=None, message_auto_delete_timer_changed=None, migrate_to_chat_id=None,
                   migrate_from_chat_id=None, pinned_message=None, invoice=None, successful_payment=None, users_shared=None, chat_shared=None,
                   connected_website=None, write_access_allowed=None, passport_data=None, proximity_alert_triggered=None, boost_added=None,
                   forum_topic_created=None, forum_topic_edited=None, forum_topic_closed=None, forum_topic_reopened=None, general_forum_topic_hidden=None,
                   general_forum_topic_unhidden=None, giveaway_created=None, giveaway=None, giveaway_winners=None, giveaway_completed=None,
                   video_chat_scheduled=None, video_chat_started=None, video_chat_ended=None, video_chat_participants_invited=None,
                   web_app_data=None, reply_markup=None, forward_date=None, forward_from=None, forward_from_chat=None,
                   forward_from_message_id=None, forward_sender_name=None, forward_signature=None, user_shared=None)


def get_update(message=None, callback=None):
    return Update(
        update_id=187,
        message=message if message else None,
        edited_message=None,
        channel_post=None,
        edited_channel_post=None,
        inline_query=None,
        chosen_inline_result=None,
        callback_query=callback if callback else None,
        shipping_query=None,
        pre_checkout_query=None,
        poll=None,
        poll_answer=None,
        my_chat_member=None,
        chat_member=None,
        chat_join_request=None
    )

