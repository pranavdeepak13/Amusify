import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
def feature_plot(features):
    labels = list(features)[:]
    stats = features.mean(axis=0).tolist()
    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    stats=np.concatenate((stats,[stats[0]]))
    angles=np.concatenate((angles,[angles[0]]))
    fig=plt.figure(figsize=(18,18))
    ax = fig.add_subplot(221, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2, label = "Track Features", color = "grey")
    ax.fill(angles, stats, alpha=0.25,facecolor='grey')
    ax.set_thetagrids(angles[0:7] * 180/np.pi, labels, fontsize = 15)
    ax.set_rlabel_position(250)
    plt.yticks([0.2,0.4,0.6,0.8], ["0.2","0.4","0.6","0.8"],color="grey", size=12)
    plt.ylim(0,1)
    ax.set_title('Track Features', fontsize=20)
    ax.grid(True)
    plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))
    st.pyplot(fig)

