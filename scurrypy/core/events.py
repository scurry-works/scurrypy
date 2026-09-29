from ..enums.events import EventType

from ..events import *


EVENTS: dict[(EventType | str), type[Event]] = {
    # startup events
    EventType.READY: ReadyEvent,

    # channel events
    EventType.CHANNEL_CREATE: ChannelCreateEvent,
    EventType.CHANNEL_UPDATE: ChannelUpdateEvent,
    EventType.CHANNEL_DELETE: ChannelDeleteEvent,
    
    EventType.CHANNEL_PINS_UPDATE: ChannelPinsUpdateEvent,

    EventType.THREAD_CREATE: ThreadCreateEvent,
    EventType.THREAD_UPDATE: ThreadUpdateEvent,
    EventType.THREAD_DELETE: ThreadDeleteEvent,
    EventType.THREAD_MEMBER_UPDATE: ThreadMemberUpdateEvent,
    EventType.THREAD_MEMBERS_UPDATE: ThreadMembersUpdateEvent,
    EventType.THREAD_LIST_SYNC: ThreadListSyncEvent,

    EventType.BULK_MESSAGE_DELETE: BulkMessageDeleteEvent,
    
    EventType.WEBHOOKS_UPDATE: WebhooksUpdateEvent,

    # invite events
    EventType.INVITE_CREATE: InviteCreateEvent,
    EventType.INVITE_DELETE: InviteDeleteEvent,

    # guild events
    EventType.GUILD_CREATE: GuildCreateEvent,
    EventType.GUILD_UPDATE: GuildUpdateEvent,
    EventType.GUILD_DELETE: GuildDeleteEvent,

    EventType.GUILD_MEMBER_ADD: GuildMemberAddEvent,
    EventType.GUILD_MEMBER_UPDATE: GuildMemberUpdateEvent,
    EventType.GUILD_MEMBER_REMOVE: GuildMemberRemoveEvent,

    EventType.GUILD_EMOJIS_UPDATE: GuildEmojisUpdateEvent,

    EventType.GUILD_STICKERS_UPDATE: GuildStickersUpdateEvent,

    EventType.GUILD_BAN_ADD: GuildBanAddEvent,
    EventType.GUILD_BAN_REMOVE: GuildBanRemoveEvent,

    # integration events
    EventType.INTEGRATION_CREATE: GuildIntegrationCreateEvent,
    EventType.GUILD_INTEGRATIONS_UPDATE: GuildIntegrationsUpdateEvent,
    EventType.INTEGRATION_UPDATE: GuildIntegrationUpdateEvent,
    EventType.INTEGRATION_DELETE: GuildIntegrationDeleteEvent,

    # interaction events
    EventType.INTERACTION_CREATE: InteractionEvent,

    # message events
    EventType.MESSAGE_CREATE: MessageCreateEvent,
    EventType.MESSAGE_UPDATE: MessageUpdateEvent,
    EventType.MESSAGE_DELETE: MessageDeleteEvent,

    # reaction events
    EventType.MESSAGE_REACTION_ADD: ReactionAddEvent,
    EventType.MESSAGE_REACTION_REMOVE: ReactionRemoveEvent,
    EventType.MESSAGE_REACTION_REMOVE_ALL: ReactionRemoveAllEvent,
    EventType.MESSAGE_REACTION_REMOVE_EMOJI: ReactionRemoveEmojiEvent,

    # role events
    EventType.ROLE_CREATE: RoleCreateEvent,
    EventType.ROLE_UPDATE: RoleUpdateEvent,
    EventType.ROLE_DELETE: RoleDeleteEvent
}
