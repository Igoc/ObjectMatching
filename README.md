# Object Matching

![badge_contributors](https://img.shields.io/github/contributors/Igoc/ObjectMatching?logoColor=red)
![badge_python](https://img.shields.io/badge/python-3-orange.svg)

#### &nbsp; Object matching with python <br/><br/>

## Example

![example](https://github.com/Igoc/ObjectMatching/blob/master/Example/Output/Cat%2002.jpg?raw=true) <br/><br/>

## Usage

```
Usage: python "Object Matching (Correlation).py" [-h] --image IMAGE --marking MARKING
                                                 [--label LABEL] [--output OUTPUT]
                                                 [--objectsize OBJECTSIZE]
                                                 [--threshold THRESHOLD]
```

```
Optional Arguments:
  -h, --help               Show help message
  --image IMAGE            Image directory path
  --marking MARKING        Marking directory path
  --label LABEL            Label directory path
  --output OUTPUT          Output directory path
  --objectsize OBJECTSIZE  Object size to set
  --threshold THRESHOLD    Threshold for correlation score
                           (-1 to 1, otherwise it will be set to average of highest correlation scores)
```

&nbsp; Match objects by pairing two images, {(I<sub>x</sub>, I<sub>x+1</sub>), x &isin; {1, 2, &#8729; &#8729; &#8729;, n - 1}}. <br/><br/>

## Data Format

### Marking

```
<Type> <Object Center X> <Object Center Y> <Object Width> <Object Height>
```

&nbsp; Marking is used to crop objects from images, Checkout [marking example](https://github.com/Igoc/ObjectMatching/tree/master/Example/Marking). <br/>
&nbsp; `<Object Center X> <Object Center Y> <Object Width> <Object Height>` is the normalized value for image size.

### Label

```
<Type> <Object Index Within Type>
```

&nbsp; Label is used for accuracy evaluation, Checkout [label example](https://github.com/Igoc/ObjectMatching/tree/master/Example/Label).