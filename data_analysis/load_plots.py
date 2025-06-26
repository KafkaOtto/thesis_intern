import matplotlib.pyplot as plt
from typing import List, Dict, Optional, Tuple
import seaborn as sns

def plot_effect_sizes(
        effect_sizes: List[float],
        labels: List[str],
        title: str,
        p_values: Optional[List[float]] = None,
        alpha: float = 0.05,
        figsize: Tuple[int, int] = (12, 6),
        palette: Dict[str, str] = None,
        font_family: str = "Arial",
        grid: bool = True,
        bar_width: float = 0.7,
        value_format: str = ".2f",
        show_legend: bool = True,
        significance_labels: bool = True
) -> None:
    """
    Enhanced visualization of effect sizes with professional styling.

    Args:
        effect_sizes: List of Cohen's d values
        labels: List of labels for each effect size
        title: Plot title
        p_values: Optional list of p-values for significance testing
        alpha: Significance threshold
        figsize: Figure dimensions
        palette: Custom color palette dictionary (keys: 'positive', 'negative', 'neutral')
        font_family: Font family for text elements
        grid: Whether to show grid lines
        bar_width: Width of bars
        value_format: Format string for effect size values
        show_legend: Whether to show legend
        significance_labels: Whether to show significance annotations
    """
    # Set default color palette
    if palette is None:
        palette = {
            'positive': '#4C72B0',  # Blue
            'negative': '#C44E52',  # Red
            'neutral': '#7F7F7F',  # Gray
            'sig_text': 'white',
            'ns_text': 'black'
        }
    # Set font properties
    plt.rcParams['font.family'] = font_family
    title_font = {'size': 14, 'weight': 'bold'}
    label_font = {'size': 12}
    tick_font = {'size': 10}

    # Create figure with constrained layout
    fig, ax = plt.subplots(figsize=figsize, layout='constrained')

    # Determine bar colors, edge colors, and text colors
    colors = []
    edge_colors = []
    text_colors = []
    annotations = []

    for d, p in zip(effect_sizes, p_values or [1.0] * len(effect_sizes)):
        if p < alpha:
            if d > 0:
                colors.append(palette['positive'])
                annotations.append("↑")
                text_colors.append(palette['sig_text'])
            elif d < 0:
                colors.append(palette['negative'])
                annotations.append("↓")
                text_colors.append(palette['sig_text'])
            else:
                colors.append(palette['neutral'])
                annotations.append("")
                text_colors.append(palette['sig_text'])
        else:
            colors.append(palette['neutral'])
            annotations.append("ns")
            text_colors.append(palette['ns_text'])
        edge_colors.append('black')

    # Create bars with improved styling
    bars = ax.bar(
        labels,
        effect_sizes,
        color=colors,
        edgecolor=edge_colors,
        linewidth=1,
        width=bar_width,
        alpha=0.85,
        zorder=2
    )

    # Add zero reference line
    ax.axhline(0, color='black', linewidth=0.8, linestyle='-', zorder=1)

    # Customize spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('black')
        ax.spines[spine].set_linewidth(0.5)

    # Set labels and title with improved styling
    ax.set_ylabel("Cohen's d Effect Size", **label_font)
    ax.set_title(title, pad=20, **title_font)

    # Rotate x-axis labels and adjust alignment
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right', **tick_font)

    # Configure grid
    if grid:
        ax.grid(axis='y', linestyle='--', alpha=0.4, zorder=0)
        ax.set_axisbelow(True)

    # Annotate bars with values and significance
    if significance_labels:
        for bar, val, ann, color in zip(bars, effect_sizes, annotations, text_colors):
            height = bar.get_height()
            va = 'bottom' if height >= 0 else 'top'
            offset = 0.02 * (1 if height >= 0 else -1)

            # Value label
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + offset,
                f"{val:{value_format}}",
                ha='center',
                va=va,
                color=color,
                fontsize=10,
                fontweight='bold'
            )

            # Significance marker (smaller, above value)
            if ann in ["↑", "↓"]:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + offset * 2,
                    ann,
                    ha='center',
                    va=va,
                    color=color,
                    fontsize=8
                )

    if show_legend:
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, fc=palette['positive'],
                          label='Significant positive effect'),
            plt.Rectangle((0, 0), 1, 1, fc=palette['negative'],
                          label='Significant negative effect'),
            plt.Rectangle((0, 0), 1, 1, fc=palette['neutral'],
                          label='Not significant')
        ]
        ax.legend(
            handles=legend_elements,
            loc='upper right',  # Places legend in upper right
            bbox_to_anchor=(1, 1),  # Anchors legend inside plot
            frameon=True,  # Adds a light border
            framealpha=0.8,  # Makes the legend slightly transparent
            edgecolor='gray',  # Border color
            fontsize=10,
        )

    # Adjust ylim to account for annotations
    y_min, y_max = ax.get_ylim()
    buffer = (y_max - y_min) * 0.1
    ax.set_ylim(y_min - buffer, y_max + buffer)

    # Add caption with statistical info
    if p_values is not None:
        caption = f"Effect sizes with Holm-Bonferroni corrected p-values (α = {alpha})"
        ax.text(
            0.5, -0.25, caption,
            ha='center', va='center',
            transform=ax.transAxes,
            fontsize=9,
            color='#555555'
        )

    # plt.show()
    plt.savefig(f"plots/{title}.png", dpi=300)

def group_label(row):
    if row['treatment'] == 't1' and row['variable'] == 'thresholds_base0.58':
        return 't1_control'
    else:
        return f"{row['treatment']}_{row['variable']}"

def load_box_plot(df):
    df['group'] = df.apply(group_label, axis=1)

    # Sort the groups so that 'tX_control' comes before its tX_variables
    from itertools import groupby

    grouped = sorted(df['group'].unique(), key=lambda x: (x.split('_')[0], x != f"{x.split('_')[0]}_control"))
    group_order = list(grouped)

    # Plot
    for metric in ['energy consumption', 'accuracy', 'latency']:
        plt.figure(figsize=(14, 6))
        sns.boxplot(data=df, x='group', y=metric, order=group_order)
        plt.xticks(rotation=45, ha='right')
        plt.title(f'Boxplot of {metric} grouped by treatment (Control on left)')

        # Optional: Add vertical lines to visually separate treatment groups
        positions = [i for i, label in enumerate(group_order) if '_control' in label and i > 0]
        for pos in positions:
            plt.axvline(x=pos - 0.5, color='gray', linestyle='--', alpha=0.5)

        plt.tight_layout()
        plt.show()