#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: WBFM cf32 to WAV
# Description: Demodulation of omur_zymyrayt_wbfm_192ksps.cf32 (complex float32, WBFM, 0 Hz baseband) to WAV without saving.
# GNU Radio version: 3.10.12.0

from gnuradio import analog
import math
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import threading




class demodulater_omur(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "WBFM cf32 to WAV", catch_exceptions=True)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 192e3
        self.freq_dev = freq_dev = 45e3
        self.gain = gain = samp_rate / (2*math.pi*freq_dev)
        self.audio_rate = audio_rate = 48000

        ##################################################
        # Blocks
        ##################################################

        self.low_pass_filter_0 = filter.fir_filter_fff(
            4,
            firdes.low_pass(
                1,
                samp_rate,
                15e3,
                3e3,
                window.WIN_HAMMING,
                6.76))
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(
            '/home/abdyrazakov/Documents/Codex/2026-09-12/referenced-chatgpt-conversation-this-is-an/outputs/fm_test_sanat.wav',
            1,
            int(audio_rate),
            blocks.FORMAT_WAV,
            blocks.FORMAT_PCM_16,
            False
            )
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/abdyrazakov/Documents/Codex/2026-09-12/referenced-chatgpt-conversation-this-is-an/outputs/guljigit_satyibekov_sanat_yiryi_wbfm_192ksps.cf32', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(gain)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_wavfile_sink_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_gain(self.samp_rate / (2*math.pi*self.freq_dev))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 15e3, 3e3, window.WIN_HAMMING, 6.76))

    def get_freq_dev(self):
        return self.freq_dev

    def set_freq_dev(self, freq_dev):
        self.freq_dev = freq_dev
        self.set_gain(self.samp_rate / (2*math.pi*self.freq_dev))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.analog_quadrature_demod_cf_0.set_gain(self.gain)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate




def main(top_block_cls=demodulater_omur, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.flowgraph_started.set()

    tb.wait()


if __name__ == '__main__':
    main()
