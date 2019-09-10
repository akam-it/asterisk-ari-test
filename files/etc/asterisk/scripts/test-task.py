#!/usr/bin/env python


import logging
import requests
import ari


logging.basicConfig(level=logging.ERROR)

client = ari.connect('http://localhost:8088', 'asterisk', 'asterisk')


def safe_hangup(channel):
    """Safely hang up the specified channel"""
    try:
        channel.hangup()
        print "Hung up {}".format(channel.json.get('name'))
    except requests.HTTPError as e:
        if e.response.status_code != requests.codes.not_found:
            raise e


def safe_bridge_destroy(bridge):
    try:
        bridge.destroy()
    except requests.HTTPError as e:
        if e.response.status_code != requests.codes.not_found:
            raise e


def stasis_start_cb(channel_obj, ev):
    endpoint = 'SIP/200'
    channel = channel_obj.get('channel')
    channel_name = channel.json.get('name')
    args = ev.get('args')

    if not args:
        print "{} entered our application".format(channel_name)
        channel.ring()

        try:
            print "Dialing {}".format(endpoint)
            outgoing = client.channels.originate(endpoint=endpoint,
                                                 app='bridge-dial',
                                                 appArgs='dialed')
        except requests.HTTPError:
            print "Whoops, pretty sure %s wasn't valid" % endpoint
            channel.hangup()
            return

        channel.on_event('StasisEnd', lambda *args: safe_hangup(outgoing))
        outgoing.on_event('StasisEnd', lambda *args: safe_hangup(channel))
    else:
        return

    def outgoing_start_cb(channel_obj, ev):
        print "{} answered; bridging with {}".format(outgoing.json.get('name'),
                                                     channel.json.get('name'))
        channel.answer()

        bridge = client.bridges.create(type='mixing')
        bridge.addChannel(channel=[channel.id, outgoing.id])

        # Clean up the bridge when done
        channel.on_event('StasisEnd', lambda *args:
                         safe_bridge_destroy(bridge))
        outgoing.on_event('StasisEnd', lambda *args:
                          safe_bridge_destroy(bridge))

    outgoing.on_event('StasisStart', outgoing_start_cb)


client.on_channel_event('StasisStart', stasis_start_cb)

client.run(apps='bridge-dial')
